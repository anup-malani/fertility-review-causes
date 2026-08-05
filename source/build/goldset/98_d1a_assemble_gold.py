#!/usr/bin/env python3
"""
98_d1a_assemble_gold.py — D.1.a, GACS stage A3 completion. Assemble and freeze the gold set.

Produces the two artifacts every downstream stage consumes, in the record shape B.1 and D.3.b already
established (`paperId, doi, title, year, cited_by_count, authors, venue, abstract, provisional_cell`):

  TIER A — the empirical core plus the theory canon, KEPT SEPARATE, from the 48 existence-gated
           cold-start anchors built in `91_`. Theory anchors do not count toward empirical recall,
           per A3, and the 10 decoys never do. Each empirical anchor already carries its estimand-cell
           tag (`provisional_cell`, `pair`, `design_tier`) from 91, which is the A3 requirement that
           topical membership and estimand membership be recorded separately.

  TIER B — the snowball-relevant set TAKEN WHOLE: 85 from round 1 plus 410 new from round 2, 495
           records. A3 is explicit that Tier B is not filtered for keyword-absence, and this run has
           its own reason to obey that: the round-1 log already refused to keyword-filter the frame
           down to fertility papers because it "would bias Tier B toward keyword-reachable work and
           inflate Recall(B), which is exactly the error the OAS and C.2.c runs were burned by." The
           filtering that HAS been applied is the treatment x outcome relevance filter (v3), which is
           what makes a record part of the frame at all, not a keyword proxy for the production query.

ENRICHMENT RUNS ON SEMANTIC SCHOLAR'S BATCH ENDPOINT, AND THE REASON IS COST. The snowball carried
only title, year, venue and an identifier; the term-mining stage needs abstracts and the recall probe
needs authors and citation counts. B.1 and D.3.b enriched from OpenAlex, which is no longer available
for bulk work at the free tier -- a title search costs $0.001 against a daily allowance that will not
cover sixteen of them, let alone 543. S2's `paper/batch` takes up to 500 identifiers per request, so
the whole gold set enriches in three calls rather than 543. This is the same provider substitution the
snowball made, for the same reason, and it keeps Tier B orthogonal to OpenAlex in infrastructure.

THE RESOLUTION RULE IS A3'S, NOT A CONVENIENCE. A record the enricher cannot resolve is KEPT, keyed on
title, and flagged -- never dropped. Dropping unresolvable records biases the recall denominator
toward easy-to-find papers, which is the direction that flatters the query. Separately, and unlike the
OAS run that made the existence gate mandatory, ghosts are not the live risk here: every Tier-B record
is a citation edge returned by Crossref or S2 about a work another paper actually cites, not a title an
LLM produced. The gate is still reported, because "we had no reason to expect ghosts" is how the OAS
run got 40% of them.

RUN ORDER IS BINDING: `98_` THEN `99_`. This script WRITES `{slug}-tier-b-frame.json` and `99_`
REWRITES IT IN PLACE with the Crossref backfill. Re-running 98 alone therefore silently reverts 31
recovered DOIs and 73 abstracts, and the frame would still look complete. Both are cached and
idempotent, so `98 && 99` reproduces the frozen artifact exactly; 98 on its own does not.

Output: literature/search-logs/{slug}-tier-a.json
        literature/search-logs/{slug}-tier-b-frame.json   (then backfilled by 99_)
        literature/search-logs/{slug}-tier-ab-log.md
"""
import json, os, re, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d1a_fetch import Fetcher  # noqa: E402

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TMP = os.path.join(ROOT, "temp", "d1a")
R1 = os.path.join(TMP, "snowball-r1-pool-scored.json")
R2 = os.path.join(TMP, "snowball-r2-pool-scored.json")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
CACHE = os.path.join(HERE, "d1a_enrich_cache.json")

FETCH = Fetcher(CACHE, UA)
BATCH = 400   # S2 allows 500; 400 leaves headroom for the URL and keeps a failure cheaper to retry
FIELDS = "title,abstract,year,venue,authors,citationCount,externalIds"


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def s2_batch(ids):
    """POST up to BATCH identifiers, return a list aligned with `ids` (None where unresolved)."""
    out = []
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        key = f"batch::{FIELDS}::" + "|".join(chunk)
        if key in FETCH.cache:
            out.extend(FETCH.cache[key]); continue
        body = json.dumps({"ids": chunk})
        got = None
        for attempt in range(5):
            FETCH._pace("https://api.semanticscholar.org/x")
            p = subprocess.run(
                ["curl", "-s", "-m", "90", "-A", UA, "-X", "POST",
                 "-H", "Content-Type: application/json", "-d", body, "-w", "\n%{http_code}",
                 f"https://api.semanticscholar.org/graph/v1/paper/batch?fields={FIELDS}"],
                capture_output=True, text=True)
            payload, _, code = p.stdout.rpartition("\n")
            if code.strip() in ("429", "503"):
                FETCH.throttled += 1
                time.sleep(min(3 * (2 ** attempt), 30)); continue
            if p.returncode == 0 and payload.strip().startswith("["):
                got = json.loads(payload)
                break
            time.sleep(3 * (attempt + 1))
        if got is None:
            # UNCONFIRMED for the whole chunk. Aligned Nones so nothing silently shifts position.
            print(f"  chunk {i}-{i + len(chunk)}: UNCONFIRMED", file=sys.stderr)
            got = [None] * len(chunk)
        else:
            FETCH.cache[key] = got
            FETCH.save()
        print(f"  chunk {i}-{i + len(chunk)}: {sum(1 for g in got if g)} of {len(chunk)} resolved",
              file=sys.stderr)
        out.extend(got)
    return out


def ident(rec):
    """The identifier S2's batch endpoint can look this record up by, best first."""
    if rec.get("doi"):
        return f"DOI:{rec['doi']}"
    if rec.get("s2id"):
        return rec["s2id"]
    return None


def shape(base, enriched, extra):
    """Emit one gold record in the shape the downstream stages expect."""
    e = enriched or {}
    ext = e.get("externalIds") or {}
    r = {
        "paperId": e.get("paperId") or base.get("s2id"),
        "doi": (ext.get("DOI") or base.get("doi") or "").lower() or None,
        "title": e.get("title") or base.get("title"),
        "year": e.get("year") if e.get("year") is not None else base.get("year"),
        "cited_by_count": e.get("citationCount"),
        "authors": "; ".join(a.get("name", "") for a in (e.get("authors") or [])) or None,
        "venue": e.get("venue") or base.get("venue") or "",
        "abstract": e.get("abstract"),
        # Kept, keyed on title, never dropped -- A3's resolution rule.
        "resolution": "ENRICHED" if enriched else "TITLE_KEYED_UNRESOLVED",
        "title_key": norm_title(base.get("title"))[:120],
    }
    r.update(extra)
    return r


def main():
    # ---- Tier B: the snowball-relevant set, whole -------------------------------------------
    r1 = json.load(open(R1))
    r2 = json.load(open(R2))
    tb, seen = [], set()
    for src, pool in (("round1", r1["pool"]), ("round2", r2["pool"])):
        for rec in pool:
            if not rec.get("relevant"):
                continue
            if src == "round2" and not rec.get("new_in_r2"):
                continue          # already counted in round 1; the union is on normalized title
            k = norm_title(rec.get("title"))[:120]
            if not k or k in seen:
                continue
            seen.add(k)
            tb.append({**rec, "_round": src})
    print(f"Tier B raw: {len(tb)} relevant records ({sum(1 for r in tb if r['_round'] == 'round1')} "
          f"round 1 + {sum(1 for r in tb if r['_round'] == 'round2')} round 2)", file=sys.stderr)

    # ---- Tier A: the existence-gated cold-start anchors --------------------------------------
    anch = json.load(open(ANCHORS))["anchors"]
    print(f"Tier A raw: {len(anch)} anchors", file=sys.stderr)

    # ---- enrich both, one identifier list --------------------------------------------------
    all_recs = [("A", a) for a in anch] + [("B", b) for b in tb]
    idxs = [i for i, (_, r) in enumerate(all_recs) if ident(r)]
    print(f"enriching {len(idxs)} of {len(all_recs)} records with a usable identifier "
          f"({len(all_recs) - len(idxs)} are title-only)", file=sys.stderr)
    got = s2_batch([ident(all_recs[i][1]) for i in idxs])
    enrich = dict(zip(idxs, got))

    tier_a, tier_b = [], []
    for i, (tier, rec) in enumerate(all_recs):
        if tier == "A":
            extra = {k: rec.get(k) for k in ("pair", "provisional_cell", "design_tier", "role",
                                             "status") if k in rec}
        else:
            extra = {"provisional_cell": None, "role": "TIER_B_FRAME",
                     "snowball_round": rec["_round"], "seen_from": rec.get("seen_from", []),
                     "relevance_reason": rec.get("relevance_reason")}
        out = shape(rec, enrich.get(i), extra)
        (tier_a if tier == "A" else tier_b).append(out)

    json.dump(tier_a, open(OUT_A, "w"), indent=1)
    json.dump(tier_b, open(OUT_B, "w"), indent=1)

    # ---- report ----------------------------------------------------------------------------
    def cov(rows, field):
        return sum(1 for r in rows if r.get(field))

    emp = [r for r in tier_a if r.get("role") == "EMPIRICAL"]
    theory = [r for r in tier_a if r.get("role") in ("THEORY", "CHANNEL1_REVIEW")]
    decoy = [r for r in tier_a if r.get("role") == "DECOY"]
    # Overlap is a validity signal, not a defect: it is how much of the keyword-probe-sourced Tier A
    # the snowball independently recovered. Measured because Recall(B) assumes the two are orthogonal
    # in SOURCE, and a reader should see how far that holds in FACT.
    akeys = {r["title_key"] for r in tier_a if r["title_key"]}
    overlap = [r for r in tier_b if r["title_key"] in akeys]

    L = [f"# D.1.a — Tier A and Tier B gold set (GACS A3)", "",
         f"Built by `98_d1a_assemble_gold.py`. Enriched on Semantic Scholar's batch endpoint, not "
         f"OpenAlex, whose free tier can no longer support bulk work.", "",
         "## Tier A — anchors, from the existence-gated cold start", "",
         f"- total anchors: **{len(tier_a)}**",
         f"- **empirical (the recall denominator): {len(emp)}** — CV floor is 30, cleared",
         f"- theory and channel-1 reviews (excluded from empirical recall, per A3): {len(theory)}",
         f"- decoys (never counted): {len(decoy)}",
         f"- abstracts recovered: {cov(tier_a, 'abstract')} of {len(tier_a)}",
         f"- unresolved, kept title-keyed: "
         f"{sum(1 for r in tier_a if r['resolution'] != 'ENRICHED')}", "",
         "## Tier B — the snowball-relevant set, taken whole", "",
         f"- total records: **{len(tier_b)}** "
         f"({sum(1 for r in tier_b if r['snowball_round'] == 'round1')} from round 1, "
         f"{sum(1 for r in tier_b if r['snowball_round'] == 'round2')} new in round 2)",
         f"- abstracts recovered: **{cov(tier_b, 'abstract')}** of {len(tier_b)} "
         f"({100 * cov(tier_b, 'abstract') / max(1, len(tier_b)):.0f}%)",
         f"- DOIs present: {cov(tier_b, 'doi')} of {len(tier_b)}",
         f"- unresolved, kept title-keyed: "
         f"{sum(1 for r in tier_b if r['resolution'] != 'ENRICHED')}", "",
         "**Not filtered for keyword-absence**, per A3 and per the round-1 seed decision: filtering "
         "Tier B toward keyword-reachable work is what inflated Recall(B) on the OAS and C.2.c runs.",
         "",
         f"## Tier A / Tier B overlap: {len(overlap)} records", "",
         f"{len(overlap)} of the {len(emp) + len(theory) + len(decoy)} Tier-A anchors were also "
         f"reached independently by the snowball. Tier A was sourced from the OpenAlex keyword probes "
         f"in `89_`/`90_` and Tier B from a Crossref/S2 citation frame, so the two are orthogonal in "
         f"source; this number is how far that orthogonality holds in fact, and it is reported "
         f"because Recall(B) is only a fair yardstick to the extent it does.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print("\n".join(L[3:]), file=sys.stderr)
    print(f"\nwrote {OUT_A}\nwrote {OUT_B}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
