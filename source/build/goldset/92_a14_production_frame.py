#!/usr/bin/env python3
"""
92_a14_production_frame.py — A.14 (coital frequency and fecundability), stage-3 production keyword frame.

The citation frame (91) is a high-precision neighbourhood (1,632) built from the classic biometric +
natural-fertility canon. This script pulls the second §5.1 Phase-1 channel — the production keyword
query from the search scope (topic AND fertility/fecundability outcome) — and MERGES it with the
citation frame into a single deduped candidate set for the blinded screen. Two channels, one frame:
the screen sees a paper once, tagged with every channel that surfaced it.

Query is the recall-oriented topic block from `literature/search-logs/coital-frequency-biological-
search-scope.md` (probe precise frame 769; recall block adds "coitus"/"sexual intercourse"): A14 topic
block AND OUTCOME. Records are pulled with abstracts inline and cached; a budget cap resumes from cache.

Output: literature/search-logs/coital-frequency-biological-screen-frame.json  (the screen input)
        appends a production-frame section to the tier-ab log.
"""
import json, os, subprocess, sys, time

SLUG = "coital-frequency-biological"
MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIERB = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT = os.path.join(LOGS, f"{SLUG}-screen-frame.json")
CACHE = os.path.join(ROOT, "temp", "a14-frame-cache.json")
SELECT = "id,doi,title,publication_year,abstract_inverted_index,cited_by_count"

# From the search scope, recall-oriented. Per the completeness test (probe 89): the precise frame is
# 769; this recall block adds the clean synonym "coitus" (+685, genuine A.14 recall for natural-fertility
# and historical-demography studies) but EXCLUDES the channel-annexing broad terms. Dropped after the
# probe: "sexual intercourse" (+1,719), "sexual activity" (+2,165), "libido" (+1,268), "sexual desire"
# (+529) — their gains are dominated by contraception / adolescent-sexuality / STI / sexual-medicine
# literature the walls route away; the frequency-focused genuine studies are already caught by "frequency
# of intercourse" + "coital frequency" + "coitus". The citation frame (91) recovers any canon studies
# outside this keyword neighbourhood; the Haiku screen (recall-first, GACS D2a) routes residual wall
# material out.
A14 = ('("coital frequency" OR "coital rate" OR "frequency of intercourse" OR "sexual frequency" '
       'OR "coitus" OR "sexual abstinence" OR "postpartum abstinence" '
       'OR "spousal separation" OR "marital separation" OR "spousal absence" OR "sexless marriage" '
       'OR "sex recession")')
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "fecundity" OR "fecundability" OR "time to pregnancy" '
           'OR "conception probability" OR "pregnancy rate")')
QUERY = f"{A14} AND {OUTCOME}"

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm  # noqa: E402  (kept for parity; abstracts reconstructed below)

cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


class BudgetExhausted(Exception):
    pass


class Refused(Exception):
    pass


def _save():
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(cache, open(CACHE, "w"), indent=0)


def oa_get(params, _retried=False):
    key = "oa::" + json.dumps(params, sort_keys=True)
    if key in cache:
        return cache[key]
    args = ["curl", "-sS", "--max-time", "120", "-G", BASE]
    for k, v in params.items():
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"mailto={MAILTO}"]
    try:
        for line in open(os.path.join(ROOT, ".env")):
            if line.startswith("OPENALEX_API_KEY="):
                k = line.split("=", 1)[1].strip().strip('"')
                if k:
                    args += ["--data-urlencode", f"api_key={k}"]
    except FileNotFoundError:
        pass
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise Refused(f"curl rc={r.returncode}: {r.stderr.strip()[:160]}")
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON body: {r.stdout[:160]!r}")
    if "error" in d:
        body = json.dumps(d)
        if "Insufficient budget" in body:
            raise BudgetExhausted(body[:200])
        if not _retried and ("Rate limit" in body or "boolean" in body):
            time.sleep(2.0)
            return oa_get(params, _retried=True)
        raise Refused(f"api error: {body[:200]}")
    cache[key] = d
    _save()
    time.sleep(0.2)
    return d


def abstract_text(inv):
    if not inv:
        return ""
    pos = [(i, w) for w, idxs in inv.items() for i in idxs]
    pos.sort()
    return " ".join(w for _, w in pos)


def main():
    # Pull the production frame by cursor, with abstracts inline.
    recs, cursor = [], "*"
    try:
        while cursor:
            d = oa_get({"filter": f"title_and_abstract.search:{QUERY}", "per-page": "200",
                        "cursor": cursor, "select": SELECT})
            recs.extend(d.get("results", []))
            cursor = (d.get("meta") or {}).get("next_cursor")
            if not d.get("results"):
                break
    except BudgetExhausted as e:
        _save()
        print(f"\nBUDGET EXHAUSTED at {len(recs)} records: {e}\nCached; re-run tomorrow to resume.",
              file=sys.stderr)
        return 2

    prod = {}
    for w in recs:
        prod[w["id"]] = {"id": w["id"], "doi": w.get("doi"), "title": w.get("title"),
                         "year": w.get("publication_year"), "cited_by_count": w.get("cited_by_count"),
                         "abstract": abstract_text(w.get("abstract_inverted_index")),
                         "source_channels": ["keyword_production"]}

    # Merge with the citation frame, deduping by OpenAlex id and unioning source channels.
    tierb = json.load(open(TIERB))
    merged = dict(prod)
    for r in tierb:
        if r["id"] in merged:
            ch = merged[r["id"]]["source_channels"]
            if r["source_channel"] not in ch:
                ch.append(r["source_channel"])
        else:
            merged[r["id"]] = {"id": r["id"], "doi": r["doi"], "title": r["title"], "year": r["year"],
                               "cited_by_count": r.get("cited_by_count"), "abstract": r["abstract"],
                               "source_channels": [r["source_channel"]]}

    frame = list(merged.values())
    json.dump(frame, open(OUT, "w"), indent=2)

    n_kw = sum(1 for r in frame if "keyword_production" in r["source_channels"])
    n_cit = sum(1 for r in frame if any(c in r["source_channels"]
                for c in ("forward_citation", "backward_reference")))
    n_both = sum(1 for r in frame if "keyword_production" in r["source_channels"]
                 and any(c in r["source_channels"] for c in ("forward_citation", "backward_reference")))
    n_abs = sum(1 for r in frame if r["abstract"])
    log = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
    with open(log, "a") as f:
        f.write("\n## Production keyword frame merged (script 92)\n\n"
                f"- Production keyword frame (topic AND outcome, verbatim from the scope): "
                f"**{len(prod)}** records.\n"
                f"- Citation frame (script 91): **{len(tierb)}**.\n"
                f"- Merged screen frame: **{len(frame)}** unique "
                f"({n_kw} keyword, {n_cit} citation, {n_both} in both); "
                f"**{n_abs}** with abstracts.\n"
                f"- Written to `{os.path.basename(OUT)}` — the blinded-screen input.\n")

    print(f"production keyword frame: {len(prod)}")
    print(f"citation frame: {len(tierb)}")
    print(f"MERGED screen frame: {len(frame)} unique ({n_kw} kw, {n_cit} cit, {n_both} both); "
          f"{n_abs} with abstracts")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
