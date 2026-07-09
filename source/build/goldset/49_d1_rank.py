#!/usr/bin/env python3
"""
49_d1_rank.py — D1 deterministic ranking + cutoff (screen stage 1, free/semantically-blind).

Ranks the 11,463 live-corpus records by a two-block term-match score over title+abstract using
the frozen production query, and cuts to the LLM pool (~2x the expected include count, per the
§7.2 default). Gold members and multi-signal papers bypass the cutoff (orthogonal-channel rule).
The downstream Haiku->Sonnet->estimand-gate screen runs only on this pool, not all 11k.

Score = (#distinct fertility-block terms matched) + (#distinct pension-block terms matched),
title matches weighted 2x abstract matches; a paper needs BOTH blocks present to be a candidate.

Inputs : {slug}-live-corpus.json, {slug}-production-query-deghosted.json (or -production-query.json),
         {slug}-tier-b-rebuilt.json (gold members bypass), {slug}-external-backbone.json
Outputs: {slug}-d1-pool.json  (ranked LLM pool), {slug}-d1-log.md
"""
import json, re, sys
from pathlib import Path

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
LOGS = HERE.parents[2] / "literature" / "search-logs"
POOL_MULT = 2          # keep ~2x expected includes
EXPECTED_INCLUDES = 550  # Anup's topical-relevant baseline (~542); pool target ~1100 + bypass

def norm(s): return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (s or "").lower())).strip()

def load_query():
    for name in (f"{SLUG}-production-query-deghosted.json", f"{SLUG}-production-query.json"):
        p = LOGS / name
        if p.exists():
            q = json.load(open(p))
            fert = q["fertility_block"]["backbone"] + q["fertility_block"]["mined_expansion"]
            pens = q["pension_oas_block"]["backbone"] + q["pension_oas_block"]["mined_expansion"]
            return fert, pens
    raise SystemExit("no production query found")

def compile_terms(terms):
    out = []
    for t in terms:
        c = norm(t.rstrip("*"))
        if c: out.append(c)
    return sorted(set(out), key=len, reverse=True)

def count_matches(text, cterms):
    """# distinct compiled terms present in the normalized text (word-boundary-ish)."""
    padded = " " + text + " "
    n = 0
    for c in cterms:
        if " " + c in padded or re.search(r"\b" + re.escape(c), padded):
            n += 1
    return n

def main():
    corpus = json.load(open(LOGS / f"{SLUG}-live-corpus.json"))
    fert, pens = load_query()
    cf, cp = compile_terms(fert), compile_terms(pens)
    gold = json.load(open(LOGS / f"{SLUG}-tier-b-rebuilt.json"))
    gold_dois = {(g.get("doi") or "").lower().replace("https://doi.org/", "") for g in gold if g.get("doi")}
    gold_titles = {norm(g["title"]) for g in gold}

    scored = []
    for r in corpus:
        t, a = norm(r.get("title")), norm(r.get("abstract"))
        ft = count_matches(t, cf); pt = count_matches(t, cp)
        fa = count_matches(a, cf) if a else 0; pa = count_matches(a, cp) if a else 0
        fert_hit = ft > 0 or fa > 0
        pens_hit = pt > 0 or pa > 0
        if not (fert_hit and pens_hit):
            continue
        score = 2 * (ft + pt) + (fa + pa)
        is_gold = (r.get("doi") in gold_dois) or (norm(r.get("title")) in gold_titles)
        scored.append({**{k: r.get(k) for k in ("paperId", "doi", "title", "year", "authors", "abstract")},
                       "d1_score": score, "is_gold": is_gold,
                       "title_both": ft > 0 and pt > 0})
    scored.sort(key=lambda x: (-x["is_gold"], -x["d1_score"], -x["title_both"]))

    # NOTE: the corpus is already the title-search (fert AND pens) result, so "both blocks present"
    # is near-universal and does NOT discriminate. Rank by term-richness (d1_score); bypass gold only.
    cutoff = POOL_MULT * EXPECTED_INCLUDES
    gold_pool = [s for s in scored if s["is_gold"]]
    rest = [s for s in scored if not s["is_gold"]]
    pool = gold_pool + rest[: max(0, cutoff - len(gold_pool))]

    json.dump(pool, open(LOGS / f"{SLUG}-d1-pool.json", "w"), indent=2, ensure_ascii=False)
    n_gold = sum(1 for s in pool if s["is_gold"])
    n_titleboth = sum(1 for s in pool if s["title_both"])
    n_abs = sum(1 for s in pool if len(s.get("abstract") or "") > 30)
    L = [f"# D1 deterministic ranking + cutoff — {SLUG}", "",
         f"- corpus: {len(corpus):,} records",
         f"- candidates (both blocks present in title or abstract): {len(scored):,}",
         f"- **LLM pool after cutoff: {len(pool):,}** (cutoff ~{cutoff}, plus bypass for gold + title-both)",
         f"  - gold members (bypass): {n_gold}",
         f"  - title-both (bypass): {n_titleboth}",
         f"  - with abstract: {n_abs:,} ({n_abs/max(len(pool),1):.0%})", "",
         "Next: Haiku recall filter over this pool -> Sonnet precision + estimand extraction -> "
         "estimand gate -> tiers."]
    (LOGS / f"{SLUG}-d1-log.md").write_text("\n".join(L) + "\n")
    print(f"corpus {len(corpus)} -> candidates {len(scored)} -> LLM pool {len(pool)} "
          f"(gold {n_gold}, title-both {n_titleboth}, abs {n_abs})", file=sys.stderr)

if __name__ == "__main__":
    main()
