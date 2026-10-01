#!/usr/bin/env python3
"""
92_a13_production_frame.py — A.13 (breastfeeding and lactational amenorrhea), stage-3 production
keyword frame.

The citation frame (91) is a high-precision neighbourhood (Tier B 998) built from the three
breastfeeding-specific identified anchors (Kennedy & Visness LAM-efficacy, Konner & Worthman
natural-fertility spacing, Howie & McNeilly suckling mechanism). This script pulls the second §5.1
Phase-1 channel — the production keyword query from the search scope — and MERGES it with the citation
frame into a single deduped candidate set for the blinded screen. Two channels, one frame: the screen
sees a paper once, tagged with every channel that surfaced it.

Query = the SPACING/AMENORRHEA-RESTRICTED channel the frame probe (89_a13) motivates (RA/PI choice,
2026-10-01). The probe found the full production frame = 5,495 but that it is inflated by the generic
fertility catch-all: bare "breastfeeding" ∧ ("fertility" OR "birth rate" OR …) annexes the enormous
breastfeeding-and-infant-health literature that merely mentions a fertility word. So the OUTCOME side is
RESTRICTED to the spacing / amenorrhea / natural-fertility / framework outcomes that are A.13's actual
estimand (the probe's "birth interval/spacing" level = 1,141 and "amenorrhea duration" = 141), dropping
the generic "fertility / birth rate / childlessness" catch-all.

Keep-and-route discipline (the A.19/A.20 move):
  * EXPOSURE side keeps the breastfeeding / suckling / amenorrhea phrasings. Bare "lactation" (+5,379,
    dairy science) and bare "nursing" (+3,135, the nursing profession) are EXCLUDED as keyword terms —
    the amenorrhea mechanism is carried by the explicit "lactational amenorrhea" phrases, and the
    lactation-physiology mechanism studies are recovered through the Howie & McNeilly CITATION FRAME.
  * The free-OR inflaters the probe priced (parity +7,859, weaning +3,147, prolactin +2,112) are
    EXCLUDED; their on-topic records carry a breastfeeding/amenorrhea phrase anyway.
Recall is maximised on A.13's spacing estimand here; the blinded screen does the precision routing, with
the A.2–A.6 contraception overlap (1,938 at frame level) as the central routing burden.

Output: literature/search-logs/breastfeeding-lactational-amenorrhea-screen-frame.json  (the screen input)
        appends a production-frame section to the tier-ab log.
"""
import json, os, subprocess, sys, time

SLUG = "breastfeeding-lactational-amenorrhea"
MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIERB = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT = os.path.join(LOGS, f"{SLUG}-screen-frame.json")
CACHE = os.path.join(ROOT, "temp", "a13-frame-cache.json")
SELECT = "id,doi,title,publication_year,abstract_inverted_index,cited_by_count"

CHANNEL = ('("breastfeeding" OR "breast feeding" OR "breast-feeding" OR "suckling" '
           'OR "exclusive breastfeeding" OR "breastfeeding duration" '
           'OR "lactational amenorrhea" OR "lactational amenorrhoea" '
           'OR "postpartum amenorrhea" OR "postpartum amenorrhoea" '
           'OR "postpartum infecundability" OR "lactational infecundability")')
OUTCOME = ('("birth interval" OR "birth intervals" OR "interbirth interval" OR "inter-birth interval" '
           'OR "birth spacing" OR "interpregnancy interval" OR "natural fertility" '
           'OR "lactational amenorrhea" OR "lactational amenorrhoea" OR "postpartum amenorrhea" '
           'OR "postpartum amenorrhoea" OR "duration of amenorrhea" OR "duration of amenorrhoea" '
           'OR "return of menses" OR "resumption of menses" OR "resumption of ovulation" '
           'OR "postpartum infecundability" OR "postpartum infecundity" OR "proximate determinants")')
QUERY = f"{CHANNEL} AND {OUTCOME}"

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
                f"- Production keyword frame (spacing/amenorrhea-restricted channel AND outcome): "
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
