#!/usr/bin/env python3
"""
410 — A.6 (TICK-087) stage 3/4: fetch the screening corpus, flag it deterministically, and stratify
it so that agent reading goes where a primary-cell study would be if one existed.

Why stratify rather than screen straight through
-------------------------------------------------
The pool is 2,815 snowball candidates plus two term arms. Screening it front-to-back would spend
most of the effort on records whose cell is not in question, and — more importantly — it would make
the chapter's conclusion depend on how far the screen happened to get. This chapter's conclusion is
an **absence** (scope §15: four channels agree `PRIMARY_NORM_FERTILITY` is empty), and the failure
mode for an absence claim is not missing a paper at random. It is concluding absence without having
looked where the paper would be.

So the corpus is flagged on title and abstract text and split into strata ordered by how plausibly a
record could be a primary-cell study. The top strata are small and are read **exhaustively**; the
long tail is sampled. That makes the absence claim a statement about the strata that could contain
the study, rather than a statement about how many batches got done.

The flags are deterministic and reproducible; they are **not** screening decisions. Nothing here
assigns a cell. `stigma scale` in an abstract makes a record likely `CONTEXT_STIGMA_MEASURE` under
rubric rule 6, but only a reader decides that (`design-is-not-a-property-of-the-title`). The flags
exist to route, and the rubric exists to decide.

Strata, in reading order
------------------------
  S1_DECISIVE     exposure + design + fertility-outcome markers. If `PRIMARY_NORM_FERTILITY` is
                  non-empty, it is here. Read exhaustively; second-read 100%.
  S2_BRIDGE       the 8 citation bridges from `409`, whatever their markers. Read exhaustively.
  S3_DESIGN_USE   exposure + design, use-outcome but no fertility outcome. The `LINK_NORM_USE`
                  candidates with an actual design. Read exhaustively.
  S4_FERT_NODESIGN exposure + fertility outcome, no design marker. Could hide a design the abstract
                  does not name. Read exhaustively if it fits, else sample hard.
  S5_EXPOSURE     exposure marker only. Sampled.
  S6_WEAK         no exposure marker. Sampled thinly; most are `OFF_OTHER`.
  S7_NOABSTRACT   no abstract in the index. Default `INSUFFICIENT_INFO` per rubric rule 8; sampled
                  on title alone, and NOT counted as excluded.

A record lands in the first stratum it qualifies for, so the strata partition the corpus.

Lessons honoured
----------------
  a-thin-cell-may-be-an-unscreened-cell — S7 is reported separately and never folded into the
      off-cell count, because a record with no abstract is missing information, not an exclusion.
  refusals-read-as-zeros — a refused metadata chunk is recorded; its records are marked
      `fetch_failed` and kept in the manifest rather than silently dropped.
  validate-a-null-detector-on-positives — the flagger is checked against the 15 resolved anchors,
      whose flags are known by hand: the stigma canon must flag exposure-without-fertility and the
      demographic canon fertility-without-stigma. A flagger that cannot reproduce `408`'s
      bifurcation is broken.

OpenAlex hazards honoured
-------------------------
  - ids are OR'd with "|" inside one filter value; filters are comma-separated and no comma appears
    inside a value
  - abstracts arrive as an inverted index and are reconstructed by position here
  - this Python has no CA bundle: shell out to curl rather than urllib
"""
import json, subprocess, sys, datetime, pathlib, time, re, random
from collections import Counter

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
TEMP = pathlib.Path("temp")
CACHE = TEMP / "a6-screen-corpus-cache.json"
POOL = LOGDIR / "a6-snowball-round1-2026-09-17.json"
ANCHORS = LOGDIR / "a6-anchor-resolution-2026-09-17.json"
SELECT = "id,display_name,publication_year,cited_by_count,authorships,abstract_inverted_index,type"
SEED = 20260917


def _api_key():
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"') or None
    except FileNotFoundError:
        pass
    return None


API_KEY = _api_key()
PACE = 0.25 if API_KEY else 1.25

MARKERS = {
    "design": [r"instrumental variable", r"\b2sls\b", r"two-stage least squares",
               r"difference-in-difference", r"differences-in-difference", r"\bdid\b design",
               r"natural experiment", r"regression discontinuity", r"\brdd\b",
               r"randomi[sz]ed controlled trial", r"\brct\b", r"cluster-randomi[sz]ed",
               r"event study", r"synthetic control", r"fixed effects", r"panel data",
               r"quasi-experiment", r"propensity score", r"instrument(?:ed|ing) ",
               r"exogenous variation", r"causal effect"],
    "fertility_outcome": [r"\bfertility\b", r"total fertility", r"\btfr\b", r"birth rate",
                          r"\bbirths\b", r"childbearing", r"\bparity\b", r"children ever born",
                          r"completed fertility", r"family size", r"number of children"],
    "use_outcome": [r"contraceptive use", r"contraceptive uptake", r"contraceptive prevalence",
                    r"unmet need", r"method use", r"\buptake\b", r"discontinuation",
                    r"contraceptive continuation", r"modern method"],
    "exposure": [r"stigma", r"taboo", r"disapprov", r"opposition", r"acceptabilit",
                 r"legitimat", r"\bshame\b", r"secrecy", r"\bnorm(?:s|ative)?\b",
                 r"religious objection", r"moral objection", r"social sanction", r"embarrass"],
    "object": [r"contracept", r"abortion", r"family planning", r"birth control",
               r"sterili[sz]ation", r"\biud\b"],
    "hiv": [r"\bhiv\b", r"\baids\b", r"sexually transmitted", r"\bsti\b", r"antiretroviral"],
    "mental": [r"mental illness", r"mental health", r"\bdepression\b", r"schizophreni",
               r"psychiatric"],
    "clinical_loss": [r"spontaneous abortion", r"miscarriage", r"pregnancy loss", r"stillbirth",
                      r"threatened abortion", r"recurrent abortion"],
    "measure_only": [r"scale development", r"validat", r"psychometric", r"conceptual framework",
                     r"framework", r"systematic review", r"scoping review", r"protocol",
                     r"editorial", r"commentary", r"research agenda", r"\bhandbook\b",
                     r"prevalence of", r"qualitative", r"focus group", r"in-depth interview",
                     r"ethnograph"],
}
COMPILED = {k: [re.compile(p, re.I) for p in v] for k, v in MARKERS.items()}


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def _cache_load():
    try:
        return json.loads(CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get(qs: str, cache: dict, _retried=False):
    if qs in cache:
        return cache[qs]
    url = f"{BASE}?{qs}&mailto={MAILTO}"
    if API_KEY:
        url += f"&api_key={API_KEY}"
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "90", url],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise Refused(f"curl exit {p.returncode}: {p.stderr.strip()[:200]}")
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON body: {p.stdout[:200]!r}")
    if "error" in d:
        msg = f"{d.get('error')} {d.get('message','')}"
        if not _retried and "rate" in msg.lower():
            time.sleep(5.0)
            return _get(qs, cache, _retried=True)
        raise Refused(f"api error: {msg}")
    cache[qs] = d
    TEMP.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))
    time.sleep(PACE)
    return d


def abstract_of(w) -> str:
    inv = w.get("abstract_inverted_index")
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def flags_for(text: str) -> dict:
    return {k: any(p.search(text) for p in ps) for k, ps in COMPILED.items()}


def stratum_of(f: dict, bridge: bool, has_abs: bool) -> str:
    # Bridges are tested BEFORE the abstract check, deliberately. A bridge with no abstract is still
    # one of the 8 records in 2,815 that cite both canons, and burying it in the sampled S7 tail
    # would let the chapter's central absence claim turn on an indexing gap. It is read on title and
    # routed to full text if the title cannot decide it.
    if bridge:
        return "S2_BRIDGE"
    if not has_abs:
        return "S7_NOABSTRACT"
    if f["exposure"] and f["design"] and f["fertility_outcome"]:
        return "S1_DECISIVE"
    if f["exposure"] and f["design"] and f["use_outcome"]:
        return "S3_DESIGN_USE"
    if f["exposure"] and f["fertility_outcome"]:
        return "S4_FERT_NODESIGN"
    if f["exposure"]:
        return "S5_EXPOSURE"
    return "S6_WEAK"


ORDER = ["S1_DECISIVE", "S2_BRIDGE", "S3_DESIGN_USE", "S4_FERT_NODESIGN",
         "S5_EXPOSURE", "S6_WEAK", "S7_NOABSTRACT"]
EXHAUSTIVE = {"S1_DECISIVE", "S2_BRIDGE", "S3_DESIGN_USE", "S4_FERT_NODESIGN"}
SAMPLE_N = {"S5_EXPOSURE": 120, "S6_WEAK": 60, "S7_NOABSTRACT": 60}


def main():
    cache = _cache_load()
    pool = json.loads(POOL.read_text())["pool"]
    bridges = {r["id"] for r in pool if r.get("bridge")}
    ids = [r["id"] for r in pool]
    by_id = {r["id"]: r for r in pool}
    refusals, corpus = [], {}

    print(f"fetching title+abstract for {len(ids)} pool records", flush=True)
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        try:
            d = _get(f"filter=openalex:{'|'.join(chunk)}&per_page=50&select={SELECT}", cache)
        except Refused as e:
            refusals.append((f"corpus chunk {i}", str(e)))
            print(f"  REFUSED chunk {i}", file=sys.stderr, flush=True)
            continue
        for w in d.get("results", []):
            wid = w["id"].rsplit("/", 1)[-1]
            corpus[wid] = w
        if i % 500 == 0:
            print(f"  {i}/{len(ids)}", flush=True)

    # positive control: the flagger must reproduce 408's bifurcation on the known anchors
    print("\npositive control — the flagger on 408's two canons", flush=True)
    anchors = [a for a in json.loads(ANCHORS.read_text())["anchors"] if a["status"] == "resolved"]
    ctrl_ids = [a["id"] for a in anchors]
    for i in range(0, len(ctrl_ids), 50):
        try:
            d = _get(f"filter=openalex:{'|'.join(ctrl_ids[i:i+50])}&per_page=50&select={SELECT}",
                     cache)
            for w in d.get("results", []):
                corpus.setdefault(w["id"].rsplit("/", 1)[-1], w)
        except Refused as e:
            refusals.append((f"control chunk {i}", str(e)))
    stig_names = {"Kumar 2009", "Norris 2011", "Cockrill 2013"}
    demo_names = {"Bongaarts 1995", "Casterline 2000", "Casterline 1997", "Sedgh 2014",
                  "Bongaarts 1991"}
    ctrl_rows, ctrl_ok = [], True
    for a in anchors:
        w = corpus.get(a["id"])
        if not w:
            continue
        f = flags_for(f"{w.get('display_name') or ''} {abstract_of(w)}")
        ctrl_rows.append({"anchor": a["asked"], "stratum": a["stratum"],
                          "exposure": f["exposure"], "fertility_outcome": f["fertility_outcome"],
                          "use_outcome": f["use_outcome"], "design": f["design"]})
        if a["asked"] in stig_names and not f["exposure"]:
            ctrl_ok = False
        if a["asked"] in demo_names and not (f["fertility_outcome"] or f["use_outcome"]):
            ctrl_ok = False
    for r in ctrl_rows:
        print(f"  {r['anchor']:<24} exp={str(r['exposure'])[:5]:<5} "
              f"fert={str(r['fertility_outcome'])[:5]:<5} use={str(r['use_outcome'])[:5]:<5} "
              f"design={str(r['design'])[:5]}", flush=True)
    print(f"  control: {'PASS' if ctrl_ok else 'FAIL'}", flush=True)
    if not ctrl_ok:
        print("  flagger cannot reproduce 408's bifurcation; refusing to stratify",
              file=sys.stderr)
        return 2

    rows = []
    for wid in ids:
        w = corpus.get(wid)
        p = by_id[wid]
        if not w:
            rows.append({"id": wid, "stratum": "S7_NOABSTRACT", "fetch_failed": True,
                         "degree": p["degree"], "bridge": bool(p.get("bridge")),
                         "title": p.get("title"), "year": p.get("year"),
                         "cited_by": p.get("cited_by"), "snippet": ""})
            continue
        title = w.get("display_name") or ""
        abst = abstract_of(w)
        f = flags_for(f"{title} {abst}")
        rows.append({"id": wid, "title": title, "year": w.get("publication_year"),
                     "cited_by": w.get("cited_by_count"), "type": w.get("type"),
                     "degree": p["degree"], "bridge": wid in bridges,
                     "seeds": p.get("seeds"), "has_abstract": bool(abst),
                     "flags": f, "fetch_failed": False,
                     "stratum": stratum_of(f, wid in bridges, bool(abst)),
                     "snippet": re.sub(r"\s+", " ", abst)[:300]})

    tally = Counter(r["stratum"] for r in rows)
    rng = random.Random(SEED)
    worklist = []
    for s in ORDER:
        members = [r for r in rows if r["stratum"] == s]
        members.sort(key=lambda r: (-(r["degree"] or 0), -(r["cited_by"] or 0)))
        if s in EXHAUSTIVE:
            chosen = members
        else:
            n = min(SAMPLE_N.get(s, 0), len(members))
            chosen = rng.sample(members, n) if n < len(members) else members
        for r in chosen:
            worklist.append({**r, "read_mode": "exhaustive" if s in EXHAUSTIVE else "sampled"})

    batches, B = [], 40
    for i in range(0, len(worklist), B):
        chunk = worklist[i:i + B]
        batches.append({"batch": len(batches) + 1, "n": len(chunk),
                        "strata": sorted({c["stratum"] for c in chunk}),
                        "ids": [c["id"] for c in chunk], "status": "pending"})

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / f"a6-screen-strata-{stamp}.json").write_text(json.dumps(
        {"generated": stamp, "script": "source/build/goldset/410_a6_screen_strata.py",
         "seed": SEED, "control_passed": ctrl_ok, "control": ctrl_rows,
         "tally": dict(tally), "sample_sizes": SAMPLE_N, "exhaustive": sorted(EXHAUSTIVE),
         "worklist_n": len(worklist), "records": rows,
         "refusals": [{"label": l, "error": e} for l, e in refusals]}, indent=1))
    (LOGDIR / "a6-screen-manifest.json").write_text(json.dumps(
        {"generated": stamp, "rubric": "stigma-reduction-contraception-abortion-screen-rubric.md",
         "batch_size": B, "batches": batches,
         "worklist": [{k: c[k] for k in ("id", "stratum", "read_mode", "degree", "title", "year",
                                         "cited_by", "snippet")} for c in worklist]}, indent=1))

    md = [f"# A.6 screening strata — {stamp}", "",
          "Generated by `source/build/goldset/410_a6_screen_strata.py`. Do not edit by hand;",
          "re-run the script.", "",
          "Flags are deterministic and **are not screening decisions** — they route reading, and the",
          f"rubric decides. Positive control on `408`'s two canons: **{'PASS' if ctrl_ok else 'FAIL'}**.",
          "", f"Pool **{len(rows):,}** · worklist **{len(worklist):,}** "
          f"(exhaustive in {', '.join(sorted(EXHAUSTIVE))}; sampled elsewhere) · "
          f"**{len(batches)}** batches of {B}", ""]
    if refusals:
        md += [f"**{len(refusals)} chunk(s) REFUSED.** Their records are marked `fetch_failed` and "
               f"kept in S7, not dropped.", ""]
    md += ["| stratum | in pool | to read | mode |", "|---|---|---|---|"]
    for s in ORDER:
        n_read = sum(1 for c in worklist if c["stratum"] == s)
        md.append(f"| `{s}` | {tally.get(s, 0):,} | {n_read:,} | "
                  f"{'exhaustive' if s in EXHAUSTIVE else 'sampled'} |")
    md += ["", "## Positive control — the flagger on the resolved anchors", "",
           "| anchor | registry stratum | exposure | fertility | use | design |",
           "|---|---|---|---|---|---|"]
    for r in ctrl_rows:
        md.append(f"| {r['anchor']} | {r['stratum']} | {r['exposure']} | "
                  f"{r['fertility_outcome']} | {r['use_outcome']} | {r['design']} |")
    s1 = [r for r in rows if r["stratum"] == "S1_DECISIVE"]
    if s1:
        md += ["", "## S1_DECISIVE in full — if the primary cell is non-empty it is here", "",
               "| id | deg | year | cites | title |", "|---|---|---|---|---|"]
        for r in sorted(s1, key=lambda r: -(r["cited_by"] or 0)):
            md.append(f"| `{r['id']}` | {r['degree']} | {r['year']} | {r['cited_by']} | "
                      f"{(r['title'] or '')[:96].replace('|', '/')} |")
    (LOGDIR / f"a6-screen-strata-{stamp}.md").write_text("\n".join(md) + "\n")

    print(f"\n{dict(tally)}")
    print(f"worklist {len(worklist)} in {len(batches)} batches of {B}")
    print(f"wrote {LOGDIR}/a6-screen-strata-{stamp}.{{json,md}} and a6-screen-manifest.json")
    if refusals:
        print(f"{len(refusals)} refusal(s)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
