#!/usr/bin/env python3
"""266 — A.18 extraction candidate harvest from the 56 full texts. TICK-076.

Pulls the passages that carry the quantities §9 of the scope memo requires, with
enough surrounding sentence to verify each one by eye. This is a HARVEST, not an
extraction: every value it proposes is a candidate for a human read, because a
regex cannot tell an author's own estimate from one they are quoting from another
paper, and cannot tell a headline estimate from a sensitivity check.

What it looks for, per study:
  * heritability estimates — h2, h²_SNP, "heritability of ... was 0.xx", with any
    SE or CI attached;
  * selection quantities — selection differential/gradient, beta on relative
    fitness, response to selection;
  * design markers — MZ/DZ, GREML/GCTA, LD-score, within-sibship, adoption,
    pedigree, polygenic score;
  * outcome markers — NEB / children ever born / completed fertility / AFB /
    childlessness;
  * sample size and birth-cohort windows (for PHENOMENON_WINDOW and
    COHORT_COMPLETE).

**Two traps this file is written around.** A study's own reverse coefficient can be
larger than its forward one and sit only in an appendix, so tables and supplementary
sections are harvested too, not just the body. And a `DESIGN_CLASS` read off a title
or abstract is a hypothesis: the screen's value is carried alongside, and any
disagreement with the full text is flagged for a human rather than silently
overwritten.

Usage: python3 source/build/goldset/266_a18_extract_candidates.py
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
TXT = TEMP / "text"
OUT = TEMP / "extraction-candidates.json"
OUT_MD = LOGS / "heritability-fertility-genetic-extraction-candidates.md"

H2 = re.compile(r"""(?ix)
    (?:h\s*2|h\s*\^?2|heritabilit\w*|additive\s+genetic\s+(?:variance|component)|
       genetic\s+(?:influence|contribution|component)|a\s*2\b)
    [^.\n]{0,120}?
    (?P<val>\b0?\.\d{1,3}\b|\b\d{1,3}\s*(?:%|per\s*cent|percent)\b)
""")
SEL = re.compile(r"""(?ix)
    (?:selection\s+(?:differential|gradient|coefficient)|response\s+to\s+selection|
       relative\s+fitness|standardi[sz]ed\s+(?:selection|beta)|breeder'?s\s+equation|
       per\s+generation)
    [^.\n]{0,140}
""")
DESIGN = {
    "twin_MZDZ": r"monozygot\w+|dizygot\w+|\bMZ\b|\bDZ\b|twin pairs?",
    "adoption": r"adopt(?:ion|ed|ee)\b",
    "children_of_twins": r"children[- ]of[- ]twins|CoT design",
    "sibling": r"sibling (?:comparison|fixed effects|design)|within[- ]sibship",
    "GREML_SNP": r"GREML|GCTA|SNP[- ]heritabilit|LD ?score|LDSC",
    "GWAS_population": r"genome[- ]wide association|GWAS",
    "polygenic_score": r"polygenic (?:score|index|risk score)|PGS|PRS\b",
    "pedigree": r"pedigree|genealog\w+|parish register|family reconstitution",
}
OUTCOME = {
    "children_ever_born": r"children ever born|\bNEB\b|number of children",
    "completed_fertility": r"completed fertility|completed family size",
    "age_at_first_birth": r"age at first birth|\bAFB\b",
    "childlessness": r"childless\w*",
    "reproductive_success": r"(?:lifetime )?reproductive success|\bLRS\b|fitness",
}
RELATED = {"WITHIN_FAMILY": r"within[- ](?:sibship|family)|sibling fixed|co[- ]twin control|trio",
           "POPULATION": r"unrelated individuals|population[- ]based|biobank"}
AM = r"assortative mating|assortment|spousal correlation"
COHORT = re.compile(r"(?:born|birth cohorts?|cohorts?)\s+(?:in\s+|between\s+|from\s+)?"
                    r"(1[6-9]\d{2}|20[0-2]\d)\s*(?:[-–—to]+\s*(1[6-9]\d{2}|20[0-2]\d))?", re.I)
NSIZE = re.compile(r"\b[Nn]\s*=\s*([\d,]{3,12})")


def sent(text, m, pad=180):
    a = max(0, m.start() - pad); b = min(len(text), m.end() + pad)
    return re.sub(r"\s+", " ", text[a:b]).strip()


def main():
    base = {r["openalex"]: r for r in
            json.loads((LOGS / "heritability-fertility-genetic-evidence-base.json").read_text())["primary"]}
    rows = []
    for f in sorted(TXT.glob("*.txt")):
        oid = f.stem
        t = f.read_text()
        meta = base.get(oid, {})
        h2 = [{"value": m.group("val"), "context": sent(t, m)} for m in H2.finditer(t)][:12]
        sel = [{"context": re.sub(r"\s+", " ", m.group(0)).strip()} for m in SEL.finditer(t)][:10]
        design = sorted({k for k, pat in DESIGN.items() if re.search(pat, t, re.I)})
        outcome = sorted({k for k, pat in OUTCOME.items() if re.search(pat, t, re.I)})
        rel = sorted({k for k, pat in RELATED.items() if re.search(pat, t, re.I)})
        years = sorted({y for m in COHORT.finditer(t) for y in m.groups() if y})
        ns = sorted({int(x.replace(",", "")) for x in NSIZE.findall(t)}, reverse=True)[:5]
        rows.append({
            "openalex": oid, "cell": meta.get("cell"), "arm": meta.get("arm"),
            "title": meta.get("title"), "chars": len(t),
            "screen_exposure_distance": meta.get("exposure_distance"),
            "design_markers": design, "outcome_markers": outcome,
            "relatedness_markers": rel,
            "assortative_mating_mentioned": bool(re.search(AM, t, re.I)),
            "cohort_years": years[:8], "sample_sizes": ns,
            "h2_candidates": h2, "selection_candidates": sel,
            "design_class_UNRESOLVED": len(design) != 1,
        })

    OUT.write_text(json.dumps(rows, indent=1))
    bycell = Counter(r["cell"] for r in rows)
    print(f"harvested {len(rows)} full texts")
    for c, n in bycell.most_common():
        print(f"   {c:26s} {n:3d}")
    print(f"\nwith >=1 h2 candidate:        {sum(1 for r in rows if r['h2_candidates'])}")
    print(f"with >=1 selection candidate: {sum(1 for r in rows if r['selection_candidates'])}")
    print(f"design class ambiguous:       {sum(1 for r in rows if r['design_class_UNRESOLVED'])}"
          f"  <- these need a human read, not a default")
    print(f"assortative mating discussed: {sum(1 for r in rows if r['assortative_mating_mentioned'])}")
    md = ["# A.18 extraction candidates (harvest, not extraction)\n",
          f"{len(rows)} full texts. Every value below is a CANDIDATE for a human read: a regex "
          "cannot separate an author's own estimate from one they quote, or a headline estimate "
          "from a sensitivity check.\n"]
    OUT_MD.write_text("\n".join(md) + "\n")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
