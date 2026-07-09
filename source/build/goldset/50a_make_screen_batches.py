#!/usr/bin/env python3
"""
50a_make_screen_batches.py — split the D1 pool into screening batches for the LLM screen.

Emits temp/screen/batch_XX.json (paperId + title + abstract + d1_score + is_gold) and a shared
RUBRIC.md, so parallel screening agents each read one batch and write one verdict file. Mirrors
the 24a/35a batch pattern.

Output: temp/screen/batch_XX.json (inputs), RUBRIC.md, manifest.json
"""
import json
from pathlib import Path

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
LOGS = HERE.parents[2] / "literature" / "search-logs"
OUT = HERE.parents[2] / "temp" / "screen"
OUT.mkdir(parents=True, exist_ok=True)
BATCH = 30

RUBRIC = """# Screening rubric — old-age-security / pension-crowdout → fertility

You are screening candidate papers for a systematic review of the **old-age-security (OAS) motive for
fertility**: the hypothesis that people have children (partly) as old-age support, so pensions / social
security / old-age transfers *crowd out* fertility. Judge each paper on its **title + abstract**.

For EACH paper return an object with these fields:

- `paperId`: copy verbatim.
- `verdict`: one of
    - `RELEVANT`      — clearly about the OAS/pension ↔ fertility relationship (empirical or theory).
    - `UNCERTAIN`     — plausibly related but title+abstract can't decide (routes to the RA gate).
    - `NOT_RELEVANT`  — not about this relationship (e.g. pensions with no fertility link, fertility
                        with no old-age-security/pension link, or an unrelated topic that merely shares
                        vocabulary).
- `estimand_cell`: one of
    - `PRIMARY`  — identifies OAS-motive / pension / social-security → **fertility**, forward direction,
                   as an **empirical estimate** (the poolable cell).
    - `THEORY`   — a formal/theoretical model of the relationship (no empirical estimate).
    - `OFF`      — real but off the primary cell: off-outcome (e.g. savings, labor supply, schooling,
                   co-residence), off-channel (e.g. grandparental childcare), or reverse direction
                   (fertility → pensions). Give the sub-reason in `off_reason`.
    - `NA`       — for NOT_RELEVANT papers.
- `outcome`: the outcome the paper measures (short phrase), or "n/a".
- `mechanism`: the mechanism/channel (short phrase), or "n/a".
- `direction`: `forward` (cause→fertility), `reverse` (fertility→cause), or `n/a`.
- `evidence_type`: `quasi-experimental` | `observational` | `structural` | `theory` | `review` | `other`.
- `off_reason`: only if estimand_cell=OFF, else "".
- `reason`: one clause justifying the verdict+cell.

Be **recall-preserving** on `verdict` (when torn between NOT_RELEVANT and UNCERTAIN, choose UNCERTAIN),
but **precise** on `estimand_cell` (PRIMARY only when it truly identifies the forward empirical effect
on fertility). Return a JSON array, one object per input paper, same order. Output ONLY the JSON array.
"""

def main():
    pool = json.load(open(LOGS / f"{SLUG}-d1-pool.json"))
    (OUT / "RUBRIC.md").write_text(RUBRIC)
    manifest = []
    for i in range(0, len(pool), BATCH):
        chunk = [{"paperId": p["paperId"], "title": p.get("title"),
                  "abstract": (p.get("abstract") or "")[:1800], "d1_score": p.get("d1_score"),
                  "is_gold": p.get("is_gold")} for p in pool[i:i+BATCH]]
        bi = i // BATCH + 1
        fn = OUT / f"batch_{bi:02d}.json"
        json.dump(chunk, open(fn, "w"), indent=2, ensure_ascii=False)
        manifest.append({"batch": bi, "input": str(fn), "output": str(OUT / f"verdict_{bi:02d}.json"),
                         "n": len(chunk)})
    json.dump(manifest, open(OUT / "manifest.json", "w"), indent=2)
    n_tot = len(pool); n_b = len(manifest)
    print(f"{n_tot} papers -> {n_b} batches of <= {BATCH} in {OUT}")

if __name__ == "__main__":
    main()
