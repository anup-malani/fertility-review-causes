#!/usr/bin/env python3
"""269 — A.18 retitled-version-pair detector. **FAILED DIAGNOSTIC — DO NOT USE ITS OUTPUT.**

Kept because the negative result is worth more than the tool: numeric fingerprinting
does NOT identify retitled version pairs in this corpus.

Measured, 2026-08-31: on the one pair known to be real — *Why do we get sick?*
(medRxiv 2025) and *Genetic trade-offs in fertility and longevity…* (Nat Ecol Evol
2026), same authors, same h2 = 0.03 (s.e. 1.4e-3) — the detector scores **zero
recall**, while emitting 18 false-positive candidates such as *The Biocultural
Origins of Human Capital Formation* paired with *Responding to a 100-Year-Old
Challenge from Fisher*. It misses the true pair because the preprint and the
published version format the same values differently (1.4 x 10-3 vs 1.4e-3), so the
fingerprints never intersect, and it fires on unrelated papers because ordinary
statistical values recur across any 56 papers in one field.

A diagnostic that scores 0 on its only known positive is not evidence about the
corpus. The confirmed pair is merged by hand and the general risk is routed to the
RA gate, where a human comparing author lists and cohorts can see what a regex
cannot.

Original intent follows.

Original docstring — A.18: find version pairs RETITLED between preprint and publication. TICK-076.

258 deduped version pairs by folded title and first author. That catches a preprint
sharing its published title, and misses the common case where a paper is retitled
on acceptance. A.18 has at least one: *Why do we get sick? Genetic evidence for
evolutionary trade-offs between fertility, longevity and disease* (medRxiv 2025)
and *Genetic trade-offs in fertility and longevity explain the maintenance of
disease-associated alleles in humans* (Nature Ecology & Evolution 2026) — same
authors, same estimate (h2 = 0.03, s.e. = 1.4e-3), no shared title tokens. Both sit
in the 148 primary studies, so that study is counted twice.

Detection is by **numeric fingerprint**: the set of distinctive decimal values a
paper reports. Two texts sharing many rare values are the same analysis whatever
they are called. Title similarity is reported alongside so the retitled cases are
visible as exactly the ones title matching would miss.

Candidates are flagged for a human read, never auto-merged: two papers from one
group on one cohort can legitimately share values.

Usage: python3 source/build/goldset/269_a18_retitled_pairs.py
"""
import json
import re
import unicodedata
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TXT = ROOT / "temp" / "a18" / "text"
OUT = LOGS / "heritability-fertility-genetic-retitled-pairs.json"
NUM = re.compile(r"(?<![\d.])[-−]?\d?\.\d{3,5}(?![\d])")


def fold(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def main():
    base = {r["openalex"]: r for r in
            json.loads((LOGS / "heritability-fertility-genetic-evidence-base.json").read_text())["primary"]}
    fp, texts = {}, {}
    for f in TXT.glob("*.txt"):
        t = f.read_text()
        vals = Counter(NUM.findall(t))
        # distinctive values only: drop ones that appear everywhere (0.05, 0.001 ...)
        fp[f.stem] = {v for v, n in vals.items() if n <= 6}
        texts[f.stem] = t
    common = Counter()
    for s in fp.values():
        for v in s:
            common[v] += 1
    rare = {v for v, n in common.items() if n <= 3}

    pairs = []
    for a, b in combinations(sorted(fp), 2):
        sh = (fp[a] & fp[b]) & rare
        if len(sh) < 8:
            continue
        ta, tb = base.get(a, {}).get("title", ""), base.get(b, {}).get("title", "")
        A, B = set(fold(ta).split()), set(fold(tb).split())
        jac = len(A & B) / len(A | B) if A | B else 0
        pairs.append({"a": a, "b": b, "shared_rare_values": len(sh),
                      "title_jaccard": round(jac, 2),
                      "title_a": ta, "title_b": tb,
                      "retitled_missed_by_title_dedup": jac < 0.3,
                      "example_shared": sorted(sh)[:8]})
    pairs.sort(key=lambda p: -p["shared_rare_values"])
    OUT.write_text(json.dumps({"summary": {
        "ticket": "TICK-076", "texts_compared": len(fp),
        "candidate_pairs": len(pairs),
        "retitled_candidates": sum(1 for p in pairs if p["retitled_missed_by_title_dedup"]),
        "note": "Numeric-fingerprint candidates for a HUMAN read, never auto-merged: two papers "
                "from one group on one cohort can legitimately share values."},
        "pairs": pairs}, indent=1))
    print(f"texts compared: {len(fp)}   candidate pairs: {len(pairs)}   "
          f"retitled (title jaccard < 0.3): {sum(1 for p in pairs if p['retitled_missed_by_title_dedup'])}")
    for p in pairs[:8]:
        flag = "  <-- RETITLED, title dedup cannot see this" if p["retitled_missed_by_title_dedup"] else ""
        print(f"\n  shared={p['shared_rare_values']:3d}  jaccard={p['title_jaccard']:.2f}{flag}")
        print(f"     A: {(p['title_a'] or '')[:82]}")
        print(f"     B: {(p['title_b'] or '')[:82]}")


if __name__ == "__main__":
    main()
