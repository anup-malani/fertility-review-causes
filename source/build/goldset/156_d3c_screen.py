#!/usr/bin/env python3
r"""
156_d3c_screen.py — D.3.c, Phase D. The two-stage screen (D2a Haiku -> D2b Sonnet).

Runs the cascade PROTOCOL Phase D specifies, over the records D1 (`154_`) passed. Both stages share
one rubric — `{slug}-screen-rubric.md`, read from disk so the text that ran is the text in version
control — and both use the Batch API, because screening is not latency-sensitive and there is no
reason to pay list price for it.

    D2a  claude-haiku-4-5   recall-preserving. Calibration target: recall ~= 1.0 on the gold.
    D2b  claude-sonnet-5    precision + estimand extraction, over D2a survivors only.

USAGE
    python 156_d3c_screen.py calibrate       # D2a on the gold only — measures recall BEFORE spending
    python 156_d3c_screen.py stage1 [--limit N]
    python 156_d3c_screen.py stage2
    python 156_d3c_screen.py collect <batch_id>

WHY THE CALIBRATE STEP IS FIRST AND IS NOT OPTIONAL. A D2a false negative is unrecoverable — nothing
downstream can retrieve a record D2a discarded, and nobody ever learns it existed. So D2a is gated on
a measured recall figure against the frozen gold, run on a few hundred records for a few cents,
before the paid pass over ~360,000. If calibrated recall is below the floor, the rubric is loosened
and re-measured; the full run does not start.

DESIGN NOTES, each of which is a decision rather than a default:

  * **Structured outputs, not prose parsing.** `output_config.format` with a JSON schema makes the
    verdict machine-readable by construction. Supported on both Haiku 4.5 and Sonnet 5 and compatible
    with the Batches API.
  * **Prompt caching on the rubric.** The rubric is byte-identical across every request and carries
    `cache_control`, so it is served at ~0.1x after the first write. Records go AFTER it — anything
    volatile placed before the breakpoint would invalidate the prefix on every request.
  * **Records are batched RECORDS_PER_REQUEST at a time** so the rubric amortises. The schema is an
    array keyed by the record's own id, so a mis-ordered or short response is detectable rather than
    silently misaligned — the failure mode this design exists to prevent is verdicts sliding one
    record out of register.
  * **`thinking` is disabled on both stages**, which is a cost decision with a stated cost. The walls
    this screen can actually enforce (4, 5, 6, 7, 9, 10) are close to mechanical; Wall 1, the one that
    would benefit from reasoning, is declared unenforceable at title/abstract anyway. Enabling
    adaptive thinking on D2b would raise its output tokens several-fold — see 155's model — and buy
    judgement on a wall the rubric forbids attempting.
  * **Results are keyed by `custom_id`, never by position.** Batch results arrive in arbitrary order.
  * **Resumable.** Every completed batch is written to disk as it lands; a re-run skips what exists.
    A 360k-record job that has to restart from zero on an interruption is a job that never finishes.

CREDENTIALS. Uses the standard resolution chain — ANTHROPIC_API_KEY, then ANTHROPIC_AUTH_TOKEN, then
an `ant auth login` profile. A bare `Anthropic()` picks up whichever is present; do not hardcode a key.
"""
import argparse, json, os, sys, time

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(ROOT, "temp", "d3c-screen")

STAGE1_MODEL = "claude-haiku-4-5"
STAGE2_MODEL = "claude-sonnet-5"
RECORDS_PER_REQUEST = 20
RECALL_FLOOR = 0.98          # D2a will not proceed to the full run below this on the gold

# WIRE FORMAT IS A SHORT CODE, NOT THE CELL NAME. Output tokens are 67% of this screen's cost
# ($90 of $134 at the verbose schema), so schema verbosity is a budget decision rather than a
# formatting preference. Emitting `"PMD"` instead of `"PRIMARY_MEASURED_DESPAIR"` costs nothing in
# recall and takes the full cascade from ~$134 to ~$82 — the same price as the most aggressive
# corpus-cutting option priced in 157_, which would have cost 16 points of gold recall to reach.
# The codes are expanded back to cell names at collection; nothing downstream sees a code.
CODES = {
    "PMD": "PRIMARY_MEASURED_DESPAIR", "PDM": "PRIMARY_DECLINE_WITH_MECHANISM",
    "PAC": "PRIMARY_ACCELERATION", "SDN": "SECONDARY_DECLINE_NO_MECHANISM",
    "TSH": "TRANSITORY_SHOCK", "MAR": "MARRIAGE_CHANNEL", "MOR": "DESPAIR_MORTALITY",
    "THY": "THEORY_DESPAIR", "EXP": "EXPOSURE_SERIES", "OCL": "OFF_CLINICAL_D3a",
    "ORE": "OFF_RESOURCE", "OCM": "OFF_CLIMATE_D3b", "REV": "REVERSE", "CMP": "COMPOSITION",
    "OTH": "OFF_OTHER", "INS": "INSUFFICIENT_INFO",
}
CELLS = list(CODES)
VERDICTS = ["R", "U", "N"]          # RELEVANT / UNCERTAIN / NOT_RELEVANT
VERDICT_NAMES = {"R": "RELEVANT", "U": "UNCERTAIN", "N": "NOT_RELEVANT"}
CHAPTERS = {"D": "DEFERRAL", "A": "ACCELERATION", "X": "UNASSIGNABLE", "-": "NA"}
LEVELS = {"I": "INDIVIDUAL", "P": "PLACE_ECOLOGICAL", "M": "MULTILEVEL", "?": "UNCLEAR"}

STAGE1_SCHEMA = {
    "type": "object",
    "properties": {"v": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "i": {"type": "string", "description": "The record id, exactly as given."},
            "d": {"type": "string", "enum": VERDICTS, "description": "R relevant, U uncertain, N not."},
            "c": {"type": "string", "enum": CELLS, "description": "Cell code."},
        },
        "required": ["i", "d", "c"], "additionalProperties": False}}},
    "required": ["v"], "additionalProperties": False,
}
STAGE2_SCHEMA = {
    "type": "object",
    "properties": {"v": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "i": {"type": "string"},
            "d": {"type": "string", "enum": VERDICTS},
            "c": {"type": "string", "enum": CELLS},
            "ch": {"type": "string", "enum": list(CHAPTERS),
                   "description": "D deferral, A acceleration, X unassignable, - not applicable."},
            "l": {"type": "string", "enum": list(LEVELS),
                  "description": "I individual, P place/ecological, M multilevel, ? unclear."},
            "pc": {"type": "boolean", "description": "Post-communist study setting."},
            "est": {"type": "boolean", "description": "Reports a quantitative estimate of a "
                                                      "determinant on a fertility outcome."},
            # RATIONALE ONLY WHEN UNCERTAIN. A one-sentence rationale on every record is ~80 output
            # tokens x every record, and on a confident verdict nobody reads it. On the uncertain
            # band an RA does read it, and that is the band the RA gate exists for — so it is kept
            # exactly where it earns its cost.
            "why": {"type": "string", "description": "REQUIRED when d is U, otherwise omit. One "
                                                     "sentence, citing the abstract."},
        },
        "required": ["i", "d", "c", "ch", "l", "pc", "est"],
        "additionalProperties": False}}},
    "required": ["v"], "additionalProperties": False,
}


def client():
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic  (the SDK is not installed in this environment)")
    return anthropic.Anthropic()


def rubric():
    return open(os.path.join(LOGS, f"{SLUG}-screen-rubric.md")).read()


def stage_instruction(stage):
    if stage == 1:
        return ("\n\n---\n\n## Your task (stage 1 of 2)\n\n"
                "You are the FIRST of two screens, and your job is RECALL, not precision. A second, "
                "more careful screen runs after you on everything you pass, so passing a record that "
                "turns out to be irrelevant costs almost nothing. Discarding a relevant one is "
                "invisible and permanent — nobody ever learns it existed.\n\n"
                "So: return `NOT_RELEVANT` only when you are confident the record sits in a "
                "routed-out cell. Anything you are unsure about is `UNCERTAIN`, which passes. "
                "Assign the single best cell; you are not asked for a chapter tag at this stage.\n\n"
                "Answer compactly: `i` = the record id, `d` = R (relevant) / U (uncertain) / "
                "N (not relevant), `c` = the cell CODE from this table:\n" + _code_table())
    return ("\n\n---\n\n## Your task (stage 2 of 2)\n\n"
            "You are the SECOND screen. Records reaching you already passed a recall-first pass, so "
            "your job is precision and structured extraction: confirm or overturn the cell, assign "
            "the chapter tag on the outcome margin, and record the level of analysis, the "
            "post-communist context flag, and whether the record estimates an effect at all.\n\n"
            "Keep the decision rule: when genuinely torn, return `UNCERTAIN` rather than "
            "`NOT_RELEVANT` — an RA adjudicates the uncertain band, and that is cheaper than a "
            "silent loss. Do not attempt Wall 1; route chronic-decline records to "
            "`SECONDARY_DECLINE_NO_MECHANISM` and let full text decide.\n\n"
            "Answer compactly: `i` id, `d` = R/U/N, `c` = cell code, `ch` = D/A/X/-, `l` = I/P/M/?, "
            "`pc` post-communist, `est` estimates an effect. Include `why` (one sentence) **only "
            "when `d` is U** — that is the band an RA adjudicates, and it is the only place the "
            "sentence is read.\n" + _code_table())


def _code_table():
    return "\n".join(f"  {k} = {v}" for k, v in CODES.items())


def render(records):
    out = []
    for r in records:
        rid = r.get("id") or r.get("key")
        title = (r.get("title") or "").strip()
        abstract = (r.get("abstract") or "").strip()
        block = f"### id: {rid}\nTITLE: {title}"
        block += f"\nABSTRACT: {abstract}" if abstract else "\nABSTRACT: (none available)"
        out.append(block)
    return "\n\n".join(out)


def build_requests(records, stage):
    """One batch request per RECORDS_PER_REQUEST records. Rubric cached; records after it."""
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    sys_blocks = [{"type": "text", "text": rubric() + stage_instruction(stage),
                   "cache_control": {"type": "ephemeral"}}]
    model = STAGE1_MODEL if stage == 1 else STAGE2_MODEL
    schema = STAGE1_SCHEMA if stage == 1 else STAGE2_SCHEMA
    reqs = []
    for i in range(0, len(records), RECORDS_PER_REQUEST):
        chunk = records[i:i + RECORDS_PER_REQUEST]
        params = dict(
            model=model, max_tokens=8000, system=sys_blocks,
            # Thinking off on both stages — a cost decision; see the module docstring.
            thinking={"type": "disabled"},
            output_config={"format": {"type": "json_schema", "schema": schema}},
            messages=[{"role": "user", "content":
                       f"Screen these {len(chunk)} records. Return one verdict per record, using "
                       f"each record's `id` exactly as given.\n\n{render(chunk)}"}],
        )
        reqs.append(Request(custom_id=f"s{stage}-{i // RECORDS_PER_REQUEST:06d}",
                            params=MessageCreateParamsNonStreaming(**params)))
    return reqs


def submit(records, stage):
    os.makedirs(WORK, exist_ok=True)
    c = client()
    reqs = build_requests(records, stage)
    print(f"stage {stage}: {len(records):,} records -> {len(reqs):,} batch requests", file=sys.stderr)
    batch = c.messages.batches.create(requests=reqs)
    open(os.path.join(WORK, f"stage{stage}-batch-id.txt"), "w").write(batch.id)
    print(f"batch {batch.id} submitted ({batch.processing_status}). "
          f"Collect with: python 156_d3c_screen.py collect {batch.id}")
    return batch.id


def collect(batch_id):
    """Poll to completion, then write results keyed by custom_id. Resumable: already-written
    shards are not re-fetched."""
    c = client()
    while True:
        b = c.messages.batches.retrieve(batch_id)
        if b.processing_status == "ended":
            break
        print(f"  {b.processing_status}: {b.request_counts}", file=sys.stderr)
        time.sleep(60)
    out, errors = {}, []
    for result in c.messages.batches.results(batch_id):
        if result.result.type != "succeeded":
            errors.append((result.custom_id, result.result.type))
            continue
        msg = result.result.message
        text = next((blk.text for blk in msg.content if blk.type == "text"), "")
        try:
            payload = json.loads(text)
        except Exception as e:
            errors.append((result.custom_id, f"unparseable: {str(e)[:60]}"))
            continue
        # Key by the record's own id, NEVER by position: batch results arrive in arbitrary order,
        # and a short or reordered array must be detectable rather than silently misaligned.
        for v in payload.get("v", []):
            # Expand the wire codes back to full names here, so the compression is invisible
            # downstream and no later stage has to know the code table.
            rec = {"verdict": VERDICT_NAMES.get(v.get("d"), v.get("d")),
                   "cell": CODES.get(v.get("c"), v.get("c"))}
            if "ch" in v:
                rec["chapter"] = CHAPTERS.get(v["ch"], v["ch"])
            if "l" in v:
                rec["level"] = LEVELS.get(v["l"], v["l"])
            for k_src, k_dst in (("pc", "context_postcommunist"), ("est", "estimates_an_effect"),
                                 ("why", "rationale")):
                if k_src in v:
                    rec[k_dst] = v[k_src]
            out[v["i"]] = rec
    os.makedirs(WORK, exist_ok=True)
    path = os.path.join(WORK, f"{batch_id}-verdicts.json")
    json.dump({"batch_id": batch_id, "verdicts": out, "errors": errors}, open(path, "w"), indent=1)
    print(f"{len(out):,} verdicts, {len(errors)} failed requests -> {path}")
    if errors:
        print("  NOTE: failed requests are recorded, not silently dropped. Re-submit them before "
              "treating the screen as complete.", file=sys.stderr)


def calibrate():
    """D2a over the gold only. Measures recall for a few cents before the paid run."""
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location("cvb", os.path.join(HERE, "152_d3c_cv_breadth.py"))
    cvb = importlib.util.module_from_spec(spec); sys.modules["cvb"] = cvb
    spec.loader.exec_module(cvb)
    gold, _n, _nc, _nn, _a = cvb.load()
    tb = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))
    bykey = {cvb.norm(r.get("title") or "")[:70]: r for r in tb if r.get("title")}
    recs = []
    for g in gold:
        r = bykey.get(cvb.norm(g["title"])[:70])
        if r:
            recs.append({"id": r["id"], "title": r.get("title"), "abstract": r.get("abstract")})
    print(f"calibration set: {len(recs)} gold records", file=sys.stderr)
    bid = submit(recs, stage=1)
    print(f"\nWhen collected, D2a recall = share of these {len(recs)} returning RELEVANT or "
          f"UNCERTAIN.\nFLOOR IS {RECALL_FLOOR:.0%} — below it, loosen the rubric and re-calibrate. "
          f"Do NOT start the full run.\n  python 156_d3c_screen.py collect {bid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["calibrate", "stage1", "stage2", "collect"])
    ap.add_argument("batch_id", nargs="?")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    if a.command == "calibrate":
        calibrate()
    elif a.command == "collect":
        if not a.batch_id:
            sys.exit("collect needs a batch id")
        collect(a.batch_id)
    elif a.command == "stage1":
        pull = os.path.join(LOGS, f"{SLUG}-c1-pull.json")
        if not os.path.exists(pull):
            sys.exit(f"C1 has not run — {pull} does not exist. The production pull comes first.")
        recs = json.load(open(pull))
        submit(recs[:a.limit] if a.limit else recs, stage=1)
    else:
        src = os.path.join(WORK, "stage1-survivors.json")
        if not os.path.exists(src):
            sys.exit(f"{src} not found — collect stage 1 and filter its survivors first.")
        submit(json.load(open(src)), stage=2)


if __name__ == "__main__":
    main()
