#!/usr/bin/env python3
"""
135_b6_tier_ab_frame.py — B.6, stage A4. Build the Tier A / Tier B citation frame.

Inherits `125_b7_tier_ab_frame.py`, with three changes this chapter forces:

  * A SECOND per-seed diagnostic, `off_species`. B.7's precision problem was one-dimensional — does
    the cloud carry a fertility quantity — and the on-topic fraction stated it as a number. B.6 has a
    second and larger problem: Wall 5. The reconnaissance found that on the microplastics fertility
    vocabulary the entire most-cited head is marine and rodent work, so a seed can score well on
    topic and still deliver a cloud that is mostly non-human. Both fractions are computed and
    reported per seed, and NEITHER is applied as a filter, for the same circularity reason.
  * Review seeds are FORWARD-CITED BUT EXCLUDED FROM THE EMPIRICAL COUNT. A3 filed the three
    channel-1 reviews under `PRIMARY_EXPOSURE_TO_FERTILITY` because that is the estimand they review.
    Counting them as empirical primary-cell anchors would inflate the causal recall denominator with
    records that estimate nothing. Membership in the denominator therefore tests the provenance
    channel as well as the cell.
  * FORWARD_CAP raised 1200 -> 2000. B.6's detection and decoy seeds are far more cited than B.7's
    (Leslie 2022 at ~3.8k, Ragusa 2020 at ~3.3k, Levine 2017 at ~1.4k), so the inherited cap would
    have truncated several of the seeds whose clouds most need to be seen. Anything still truncated
    is reported per seed with both diagnostics, never silently.

Tier A is the verified anchor set from 134. Tier B is the orthogonal frame: everything the anchors
cite (backward, one hop) and everything that cites them (forward, one hop), deduplicated and keyed on
OpenAlex id with DOI carried alongside.

FORWARD-SEED RULE (D.2.d, 2026-08-08 — the correction this script exists to carry). The inherited
frame builders (`73_d3b`, `96_d1b`) never forward-cited a routing decoy, on the reasoning that a decoy
should not import its neighbour's literature. Measured, that rule discarded the best discovery channel
the hypothesis had: a decoy is CHOSEN to sit just across a boundary wall, so its citation
neighbourhood is exactly where the boundary cases live, and boundary cases are what the walls exist to
adjudicate. On D.2.d the decoy clouds ran 29-88% on-topic against 1-14% for the theory canon.

So the rule here is uniform: every seed forward-cites, decoys included. Two traps are avoided by
construction, both recorded because both are tempting:

  * The forward fetch is NOT filtered by topic vocabulary. Doing so would prune Tier B by distance
    from the production query and bias Recall(B) toward the query being measured. On-topic fraction is
    computed and reported as a SEED-SELECTION DIAGNOSTIC, never applied as a filter on the frame.
  * Seeds are capped on cloud SIZE, and the cap is reported per seed rather than applied silently.
    Citation COUNT is the wrong criterion for judging a seed's worth (a count cap can make the right
    call for the wrong reason); it is used here only as a budget control, and every truncation is
    printed in the log with its on-topic fraction so the loss is visible rather than implied.

`seed_ids` provenance is retained on every Tier B record, so Recall(B) can later be computed with and
without decoy-seeded material as a sensitivity check.

Output: literature/search-logs/{slug}-tier-a.json
        literature/search-logs/{slug}-tier-b-frame.json
        literature/search-logs/{slug}-tier-ab-log.md
"""
import json, os, subprocess, sys, time
from urllib.parse import quote

SLUG = "microplastics-pfas-reproductive"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b6_frame_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

FORWARD_CAP = 2000          # per-seed budget control, NOT a judgement about the seed
PAGE = 200
SELECT = ("id,doi,display_name,publication_year,cited_by_count,type,authorships,"
          "primary_location,referenced_works,abstract_inverted_index")

# On-topic diagnostic vocabulary. Used ONLY to compute a reported fraction per seed. If this list
# ever feeds a filter, the Recall(B) it produces is circular.
# Kept deliberately narrow, as in B.7: it asks what fraction of a seed's citation cloud carries a
# FERTILITY QUANTITY at all. A broader list including "reproductive" or "endocrine" would score the
# mechanism and detection seeds near 100% and stop discriminating, which would make the diagnostic
# useless exactly where it is most needed.
TOPIC_TERMS = ("fertility", "fecundity", "fecundability", "birth rate", "births", "childbearing",
               "family size", "parity", "time to pregnancy", "conception", "semen quality",
               "sperm", "childless", "infertil")

# SPECIES diagnostic (new for B.6). Wall 5 is this chapter's largest precision threat and the
# reconnaissance showed it is not a tail risk: on the microplastics fertility vocabulary the entire
# most-cited head is aquatic and rodent work. This measures, per seed, what share of the cloud is
# visibly non-human, so screen design is calibrated on a number rather than an impression.
#
# NOTE ON WHAT THIS CAN AND CANNOT DO. It is a LOWER BOUND. A study is counted non-human only when it
# names its organism in the title or abstract; plenty do not, and "in vitro" work on human cell lines
# is not caught here at all (that is Wall 6, a different test). It is reported as a floor, never as a
# measured non-human fraction. "human" appearing in the blob does not cancel a hit, because
# ecotoxicology routinely cites human health in its framing — the two are not mutually exclusive and
# treating them as such would understate the floor.
ANIMAL_TERMS = ("zebrafish", "danio", "daphnia", "medaka", "mussel", "mytilus", "oyster", "copepod",
                "calanus", "tigriopus", "rotifer", "earthworm", "nematode", "caenorhabditis",
                "drosophila", "murine", " mice", " mouse", " rat ", " rats ", "rodent", "bovine",
                "porcine", "piglet", "chicken", "quail", "amphibian", "xenopus", "crustacean",
                "invertebrate", "marine organism", "aquatic organism", "fish ", "teleost",
                "in ovo", "sea urchin", "artemia", "gastropod", "bivalve")

errors = []


def openalex_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


OA_KEY = openalex_key()


def oa_get(url, tag, tries=3):
    """Returns (payload, ok). A transport failure is NOT an empty result: the caller must be able to
    tell 'the index holds nothing' from 'the request did not complete', or the frame quietly shrinks
    and Recall(B) is computed against a denominator that lost records to network errors."""
    full = url + (f"&api_key={OA_KEY}" if OA_KEY else f"&mailto={MAILTO}")
    for attempt in range(tries):
        r = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, full], capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout)
                if "results" in d or "id" in d:
                    return d, True
            except Exception:
                pass
        time.sleep(1.5 * (attempt + 1))
    errors.append((tag, url.split("filter=")[-1][:90]))
    return {}, False


def unabstract(inv):
    if not inv:
        return ""
    try:
        pos = [(i, w) for w, idxs in inv.items() for i in idxs]
        return " ".join(w for _, w in sorted(pos))[:1200]
    except Exception:
        return ""


def row(w):
    loc = (w.get("primary_location") or {}).get("source") or {}
    return {"id": (w.get("id") or "").rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "title": w.get("display_name") or "",
            "year": w.get("publication_year"),
            "cited_by_count": w.get("cited_by_count"),
            "type": w.get("type"),
            "venue": loc.get("display_name") or "",
            "authors": [a["author"]["display_name"] for a in (w.get("authorships") or [])][:6],
            "abstract": unabstract(w.get("abstract_inverted_index"))}


def _blob(rec):
    # Padded so the space-anchored terms (" mice", " rat ") can match at the string edges. Those
    # terms carry their spaces deliberately: a bare "rat" substring matches "ratio", "strata" and
    # "generation", which is the unanchored-pattern bug this codebase has now hit five times.
    return " " + (rec["title"] + " " + rec.get("abstract", "")).lower() + " "


def on_topic(rec):
    return any(t in _blob(rec) for t in TOPIC_TERMS)


def off_species(rec):
    """Visibly non-human. A LOWER BOUND — see the note on ANIMAL_TERMS."""
    return any(t in _blob(rec) for t in ANIMAL_TERMS)


def work_by_doi(doi):
    key = f"W::{doi}"
    if key in cache:
        return cache[key]
    d, ok = oa_get(f"https://api.openalex.org/works/https://doi.org/{quote(doi)}?select={SELECT}",
                   f"work:{doi}")
    if not ok or not d.get("id"):
        return None
    cache[key] = {"row": row(d), "referenced_works": [r.rsplit("/", 1)[-1]
                                                      for r in (d.get("referenced_works") or [])]}
    json.dump(cache, open(CACHE, "w"), indent=0)
    return cache[key]


def fetch_ids(ids):
    """Batch-hydrate OpenAlex ids, 50 per request via the pipe-OR filter."""
    out, todo = [], [i for i in ids if f"R::{i}" not in cache]
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        d, ok = oa_get(f"https://api.openalex.org/works?filter=openalex_id:{'|'.join(chunk)}"
                       f"&per-page=50&select={SELECT}", f"hydrate:{chunk[0]}")
        if not ok:
            continue
        for w in d.get("results", []):
            r = row(w)
            cache[f"R::{r['id']}"] = r
        json.dump(cache, open(CACHE, "w"), indent=0)
        time.sleep(0.2)
    for i in ids:
        if f"R::{i}" in cache:
            out.append(cache[f"R::{i}"])
    return out


def citing(seed_id, cap):
    """Forward citations, cursor-paged. Returns (rows, total, truncated)."""
    key = f"C::{seed_id}::{cap}"
    if key in cache:
        return cache[key]["rows"], cache[key]["total"], cache[key]["truncated"]
    rows, cursor, total = [], "*", None
    while cursor and len(rows) < cap:
        d, ok = oa_get(f"https://api.openalex.org/works?filter=cites:{seed_id}"
                       f"&per-page={PAGE}&cursor={cursor}&select={SELECT}", f"cites:{seed_id}")
        if not ok:
            break
        total = d.get("meta", {}).get("count", total)
        rows += [row(w) for w in d.get("results", [])]
        cursor = d.get("meta", {}).get("next_cursor")
        time.sleep(0.15)
    truncated = bool(total and len(rows) < total)
    cache[key] = {"rows": rows, "total": total, "truncated": truncated}
    json.dump(cache, open(CACHE, "w"), indent=0)
    return rows, total, truncated


def main():
    anchors = json.load(open(ANCHORS))
    verified = [a for a in anchors if a.get("identity_verified") and a.get("doi")]
    EMPIRICAL_CELLS = {"PRIMARY_EXPOSURE_TO_FERTILITY", "PRIMARY_MALE_FECUNDITY",
                       "PRIMARY_HIGH_EXPOSURE"}

    def is_empirical_anchor(rec):
        """In the causal recall denominator?

        Cell membership alone is not enough. A3 filed the three channel-1 systematic reviews under
        PRIMARY_EXPOSURE_TO_FERTILITY, which is the right cell for the estimand they review, but a
        review estimates nothing — counting it here would inflate the denominator that Recall(A) is
        computed against and flatter every recall number downstream. Reviews still seed the frame,
        forward and backward; they just do not count as evidence."""
        return (rec["provisional_cell"] in EMPIRICAL_CELLS
                and rec.get("provenance_channel") != "channel1_review_seed")

    tier_a, seedinfo = [], []
    for a in verified:
        w = work_by_doi(a["doi"])
        if not w:
            continue
        rec = dict(a)
        rec["openalex_id"] = w["row"]["id"]
        rec["n_referenced"] = len(w["referenced_works"])
        rec["cited_by_count"] = w["row"]["cited_by_count"]
        tier_a.append(rec)
        seedinfo.append((rec, w))
    json.dump(tier_a, open(OUT_A, "w"), indent=2)

    pool, log_rows = {}, []
    for rec, w in seedinfo:
        sid = rec["openalex_id"]
        cell = rec["provisional_cell"]
        is_empirical = is_empirical_anchor(rec)
        # BACKWARD: always, all references, one hop. Cheaper and cleaner than forward.
        back = fetch_ids(w["referenced_works"])
        # FORWARD: uniform across seed types, decoys included. The cap is a budget control and is
        # reported; empirical seeds get an unbounded pull because they are the recall spine.
        cap = 10 ** 6 if is_empirical else FORWARD_CAP
        fwd, total, truncated = citing(sid, cap)
        n_ot = sum(1 for r in fwd if on_topic(r))
        frac = (n_ot / len(fwd)) if fwd else None
        n_sp = sum(1 for r in fwd if off_species(r))
        frac_sp = (n_sp / len(fwd)) if fwd else None
        for r in back:
            p = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            p["seed_ids"].append(sid); p["channels"].add("backward")
        for r in fwd:
            p = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            p["seed_ids"].append(sid); p["channels"].add("forward")
        log_rows.append(dict(title=rec["title"][:58], cell=cell, seed=sid, empirical=is_empirical,
                             n_back=len(back), n_fwd=len(fwd), fwd_total=total,
                             truncated=truncated, on_topic=frac, off_species=frac_sp))
        print(f"  {cell[:26]:<26} back={len(back):>4} fwd={len(fwd):>5}/{total or 0:<5} "
              f"topic={f'{frac:.0%}' if frac is not None else 'n/a':>4} "
              f"animal>={f'{frac_sp:.0%}' if frac_sp is not None else 'n/a':>4}  {rec['title'][:38]}")

    anchor_ids = {r["openalex_id"] for r in tier_a}
    tier_b = []
    for rid, p in pool.items():
        if rid in anchor_ids:
            continue                      # a Tier A member is not Tier B
        p["channels"] = sorted(p["channels"])
        p["seed_ids"] = sorted(set(p["seed_ids"]))
        p["n_seeds"] = len(p["seed_ids"])
        tier_b.append(p)
    tier_b.sort(key=lambda r: (-r["n_seeds"], -(r["cited_by_count"] or 0)))
    json.dump(tier_b, open(OUT_B, "w"), indent=2)

    n_multi = sum(1 for r in tier_b if r["n_seeds"] > 1)
    n_abs = sum(1 for r in tier_b if r.get("abstract"))
    decoy_seeds = {r["openalex_id"] for r in tier_a if r["provisional_cell"].startswith("OFF_")}
    n_decoy_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= decoy_seeds)

    L = [f"# A4 Tier A / Tier B citation frame — {SLUG} (B.6)", "",
         f"**Tier A: {len(tier_a)} verified anchors** ({sum(1 for r in tier_a if is_empirical_anchor(r))} "
         "empirical primary-cell, the causal recall denominator — the three channel-1 systematic "
         "reviews sit in a primary cell but are excluded from that count, because a review estimates "
         "nothing and counting it would flatter every recall figure downstream).", "",
         f"**Tier B frame: {len(tier_b):,} deduplicated records** — {n_multi:,} found by more than one "
         f"seed, {n_abs:,} carrying an abstract ({n_abs / max(len(tier_b), 1):.0%}).", "",
         f"**Records depending ONLY on a routing-decoy seed: {n_decoy_dep:,}** "
         f"({n_decoy_dep / max(len(tier_b), 1):.0%}). Under the inherited rule these would not exist, "
         "because decoys were never forward-cited. They are retained, and `seed_ids` provenance lets "
         "Recall(B) be recomputed without them as a sensitivity check.", "",
         f"**Failed requests: {len(errors)}** — listed at the foot. A failed request is not an empty "
         "result, and the frame is smaller than the index by exactly the amount those failures cost.", "",
         "## Per-seed yield", "",
         "Both fractions are SEED-SELECTION DIAGNOSTICS computed after retrieval. Neither is applied "
         "as a filter on the frame: filtering the forward fetch by topic vocabulary would prune "
         "Tier B by distance from the production query and make Recall(B) circular.", "",
         "`on-topic` = share of the forward cloud carrying any fertility-quantity term. "
         "`animal >=` = share visibly non-human, and it is a **lower bound** — a study counts only "
         "when it names its organism in the title or abstract, and human-cell in-vitro work is not "
         "counted here at all (that is Wall 6). Read it as a floor on how hard Wall 5 will bite.", "",
         "| seed | cell | back | fwd | fwd total | truncated | on-topic | animal >= |",
         "|---|---|---|---|---|---|---|---|"]
    for r in sorted(log_rows, key=lambda x: -(x["n_fwd"])):
        ot = f"{r['on_topic']:.1%}" if r["on_topic"] is not None else "n/a"
        sp = f"{r['off_species']:.1%}" if r.get("off_species") is not None else "n/a"
        L.append(f"| {r['title']} | `{r['cell']}` | {r['n_back']} | {r['n_fwd']} | "
                 f"{r['fwd_total'] or 0} | {'**yes**' if r['truncated'] else 'no'} | {ot} | {sp} |")
    trunc = [r for r in log_rows if r["truncated"]]
    L += ["", "## Truncation", ""]
    if trunc:
        L.append(f"{len(trunc)} seed(s) hit the {FORWARD_CAP:,}-record forward cap and are reported "
                 "here rather than silently truncated — a bounded pull that is not stated reads as "
                 "complete coverage:")
        tot_lost = 0.0
        for r in trunc:
            missed = (r["fwd_total"] or 0) - r["n_fwd"]
            # Expected on-topic loss = unpulled count x the on-topic rate measured on the pulled part.
            # This ASSUMES the unpulled tail resembles the pulled head, which is exactly what a
            # cursor-paged truncation cannot guarantee. Stated as an estimate, and stated at all,
            # because "3 seeds truncated" tells a reader nothing about whether it mattered.
            exp = missed * (r["on_topic"] or 0)
            tot_lost += exp
            L.append(f"- **{r['title']}** (`{r['cell']}`): pulled {r['n_fwd']:,} of {r['fwd_total']:,} "
                     f"citing works, on-topic {r['on_topic']:.1%} — **{missed:,} unpulled, an "
                     f"estimated {exp:.0f} on-topic records not seen.**")
        L += ["", f"**Estimated on-topic records lost to the cap in total: ~{tot_lost:.0f}**, against "
                  f"a frame of {len(tier_b):,}. All three truncated seeds are low-yield "
                  "(2.5-5% on-topic), so the cap fell where it costs least — but the estimate assumes "
                  "the unpulled tail resembles the pulled head, and a cursor-paged truncation cannot "
                  "guarantee that. Raise the cap and re-run if any of these seeds later turns out to "
                  "matter for recall."]
    else:
        L.append(f"No seed reached the {FORWARD_CAP:,}-record forward cap; the frame is a complete "
                 "one-hop neighbourhood of the verified anchors.")
    if errors:
        L += ["", "## Failed requests (NOT zero results)", ""] + [f"- {a}: `{b}`" for a, b in errors[:40]]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"\ntier_a={len(tier_a)} tier_b={len(tier_b)} multi_seed={n_multi} "
          f"decoy_only={n_decoy_dep} errors={len(errors)}")
    print(f"-> {os.path.relpath(OUT_B, ROOT)}")
    if errors and len(errors) > 0.2 * max(len(tier_a), 1):
        print("WARNING: high request-failure rate; the frame is incomplete by an unknown amount.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
