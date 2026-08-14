#!/usr/bin/env python3
"""
137_b6_make_screen_batches.py — B.6, stage D2. Prepare the semantic screen.

Inherits `127_b7_make_screen_batches.py`. Writes the screening rubric and cuts the D1 worklist into
fixed batches carrying only what a title/abstract screen is entitled to see: title, venue, year,
type, and a truncated abstract.

WITHHELD FROM THE SCREENING RECORD, deliberately:
  * the D1 score and the discovery channel, as in B.7 — a screener who can see the blind sieve's rank
    will anchor on it, which collapses two independent sieves into one;
  * the deterministic `chemical_family` tag. This one is new. The tag is a fact rather than a
    judgement (the compound is named), so withholding it costs the screener almost nothing — and it
    buys a free cross-check: the screener assigns the family independently and assembly compares the
    two. Disagreement flags records where the title names one family and the study measures another,
    which is exactly the shape of a Wall 1 mixture case that the term-match cannot see.

Output: source/build/goldset/b6_screen_batches/batch_NN.json
        literature/search-logs/{slug}-screen-rubric.md
"""
import json, os

SLUG = "microplastics-pfas-reproductive"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
BATCH_DIR = os.path.join(HERE, "b6_screen_batches")
OUT_RUBRIC = os.path.join(LOGS, f"{SLUG}-screen-rubric.md")

BATCH_SIZE = 60
ABSTRACT_WORDS = 60

CELLS = [
    ("PRIMARY_EXPOSURE_TO_FERTILITY", "Measured MP or PFAS exposure -> a FERTILITY quantity in humans: births, completed parity, TFR, time-to-pregnancy, fecundability. The identification-bearing cell."),
    ("PRIMARY_MALE_FECUNDITY", "Measured exposure -> a measured MALE fertility outcome (pregnancies achieved, TTP), not a semen parameter alone."),
    ("PRIMARY_HIGH_EXPOSURE", "Contaminated-community or occupational exposure -> a fertility quantity. Ronneby, Veneto, C8, fluorochemical workers. Transport-flagged, never pooled with general-population estimates."),
    ("SEMEN_PARAMETER", "Measured exposure -> sperm count, concentration, motility, morphology. An INPUT to fertility, not a fertility quantity."),
    ("OVARIAN_PARAMETER", "Measured exposure -> AMH, antral follicle count, ovarian reserve, cycle characteristics. As above."),
    ("DETECTION_TISSUE", "Concentration of MP or PFAS MEASURED IN a human tissue or fluid, with NO outcome estimated. Placenta, follicular fluid, semen, blood. Presence is exposure, not effect: no causal recall credit."),
    ("MECHANISM_INVITRO", "Exposure of human or animal CELLS -> a cellular or molecular endpoint. Wall 6. Human-cell work passes the species check and would otherwise read as human evidence."),
    ("PARAMETER_EXPOSURE", "Population exposure levels, serum concentration trends, intake estimates, production series. Feeds demographic significance; no recall credit."),
    ("PARAMETER_PHARMACOKINETIC", "Half-life, elimination, transplacental or lactational transfer, DETERMINANTS of serum level (incl. parity). Load-bearing for the reverse-causation correction."),
    ("PARAMETER_DETERMINANT_TO_LOSS", "Measured exposure -> fetal loss, with NO fertility outcome. Cross-filed to B.5; neither chapter's recall."),
    ("MEASUREMENT_METHOD", "Detection methodology, procedural blanks and contamination control, spectroscopic identification, exposure misclassification. Load-bearing for risk of bias."),
    ("MIXTURE_UNSEPARABLE", "A joint exposure index spanning B.6 families AND B.2 families (phthalates, bisphenols, organochlorines) with no compound-specific estimate recoverable. Wall 1. Retained, pooled in neither chapter."),
    ("OUTCOME_TREND_UNATTRIBUTED", "A temporal trend in semen quality or fertility with NO exposure measured. Wall 7. It is the phenomenon the hypotheses compete to explain, not evidence for any of them."),
    ("OFF_PREGNANCY_SAFETY", "Sample conditioned on pregnancy; outcome is a property of a birth that occurred -- birth weight, gestational age, preterm, congenital anomaly, neurodevelopment. Wall 2, and large."),
    ("OFF_ART_A17", "Measured exposure in ART where the ESTIMAND is treatment success (cycle outcome, fertilisation rate, embryo quality). Wall 4. Note detection studies in ART populations are DETECTION_TISSUE, not this."),
    ("OFF_FETAL_LOSS_B5", "Measured exposure -> fetal loss WITH a fertility consequence estimated. B.5 claims it."),
    ("OFF_LEGACY_EDC_B2", "The exposure is a legacy EDC -- phthalate, bisphenol, organochlorine, DDT, solvent -- and NOT an MP/PFAS compound. Wall 1. B.2's."),
    ("OFF_ANIMAL", "Non-human exposure: fish, invertebrates, rodents, livestock, wildlife. Wall 5, and the DEFAULT occupant of this chapter's fecundity vocabulary."),
    ("OFF_SOIL_FERTILITY", "'Fertility' meaning soil or agronomic fertility. Wall 8. Cheap, but it poisons the outcome axis specifically."),
    ("OFF_ENVIRONMENTAL_FATE", "Occurrence, transport, degradation, remediation, water treatment, sampling of environmental media. The largest cell in the corpus overall."),
    ("OFF_OUTCOME", "Measured exposure -> a non-fertility, non-reproductive human outcome: thyroid, lipids, immune, cancer, kidney."),
    ("ROUTING_DEFERRED_TO_FULLTEXT", "Routing turns on mixture separability or on parity handling and the abstract does not say."),
    ("REVERSE", "Parity, pregnancy or lactation as a DETERMINANT of measured exposure. The chapter's central identification threat, and context rather than evidence."),
    ("OFF_OTHER", "A non-B.6 fertility determinant with no sibling-hypothesis home."),
    ("INSUFFICIENT_INFO", "Cannot be routed on the visible record. Pairs only with UNCERTAIN."),
]


def main():
    work = json.load(open(WORK))
    os.makedirs(BATCH_DIR, exist_ok=True)
    for f in os.listdir(BATCH_DIR):
        if f.startswith("batch_"):
            os.remove(os.path.join(BATCH_DIR, f))

    n = 0
    for i in range(0, len(work), BATCH_SIZE):
        chunk = work[i:i + BATCH_SIZE]
        recs = []
        for r in chunk:
            abs_ = " ".join((r.get("abstract") or "").split()[:ABSTRACT_WORDS])
            recs.append({"id": r["id"], "year": r.get("year"), "venue": (r.get("venue") or "")[:44],
                         "type": r.get("type"), "title": r["title"], "abstract": abs_})
        n += 1
        json.dump({"batch": n, "n": len(recs), "records": recs},
                  open(os.path.join(BATCH_DIR, f"batch_{n:02d}.json"), "w"), indent=1)

    L = [f"# Screening rubric — {SLUG} (B.6)", "",
         "Title/abstract screen over the D1 worklist. The screener sees title, venue, year, type and "
         "a truncated abstract, and does NOT see the D1 score, the discovery channel, or the "
         "deterministic chemical-family tag.", "",
         "## What the screen decides", "",
         "For each record emit `{id, verdict, cell, family, note?}` where `verdict` is one of "
         "`RELEVANT` / `UNCERTAIN` / `NOT_RELEVANT`, `cell` is one of the cells below, and `family` "
         "is `pfas` / `plastic` / `both` / `none` / `unclear`.", "",
         "**`family` is assigned independently and is cross-checked at assembly** against the "
         "deterministic tag D1 computed from the named compound. Disagreement is not an error to be "
         "suppressed — it flags records where the title names one family and the study measures "
         "another, which is the shape of a Wall 1 mixture case a term-match cannot see.", "",
         "**The screen assigns a routing cell only.** It does NOT assign `PARITY_HANDLING`, "
         "`BLANK_CONTROL`, `ESTIMAND_LEVEL` or mixture separability. All four are methods facts, "
         "invisible in an abstract, and are set at full-text extraction. The scope document commits "
         "to this in advance rather than discovering it in an audit.", "",
         "**Route on what is MEASURED, not on what is mentioned.** B.6 owns two chemical families "
         "whose names appear across two of the largest environmental literatures in existence. A "
         "record naming PFAS or microplastics is not thereby a B.6 record: ask what quantity the "
         "estimate is of, in what species, and whether MP/PFAS exposure is what varies.", "",
         "**Check species on EVERY record.** Do not infer it from topic. On the reconnaissance probes "
         "the most-cited records for microplastics paired with 'reproduction' and 'fecundity' were "
         "oysters, copepods, rotifers and mice. `OFF_ANIMAL` is the DEFAULT reading of an unqualified "
         "claim that microplastics reduce fecundity, not an afterthought. The A4 frame put the "
         "visibly-non-human floor at 6-42% across every seed cloud, PFAS clouds included.", "",
         "**Detection is not effect.** A study reporting that particles were found in placenta, "
         "follicular fluid or semen, without estimating an outcome, is `DETECTION_TISSUE` and is "
         "`RELEVANT` — but it earns no causal recall credit and must never be routed to a PRIMARY "
         "cell. This is the single most likely misroute in this chapter, because those papers are "
         "highly cited, recent, and titled as though they were about fertility.", "",
         "**Defer rather than guess.** Where routing turns on mixture separability or on parity "
         "handling and the abstract is silent, use `ROUTING_DEFERRED_TO_FULLTEXT`. An exclusion an "
         "abstract could not support is a silent false negative.", "",
         "## Cells", "", "| cell | definition |", "|---|---|"]
    for c, d in CELLS:
        L.append(f"| `{c}` | {d} |")
    L += ["", "## Verdict convention", "",
          "- `RELEVANT` — a primary, parameter, measurement, detection, mechanism or context cell. "
          "Parameter, measurement, detection and mechanism records are RELEVANT and separated "
          "downstream; they earn no empirical recall credit.",
          "- `UNCERTAIN` — routing or eligibility genuinely unclear on the visible record. Pairs with "
          "`INSUFFICIENT_INFO` or with `ROUTING_DEFERRED_TO_FULLTEXT`.",
          "- `NOT_RELEVANT` — an `OFF_*` cell, including the very large environmental-fate, "
          "pregnancy-safety and non-human literatures.", "",
          "## Batches", "", f"{n} batches of up to {BATCH_SIZE} records, {len(work)} records total, "
          f"abstracts truncated to {ABSTRACT_WORDS} words."]
    open(OUT_RUBRIC, "w").write("\n".join(L) + "\n")
    print(f"records={len(work)} batches={n} -> {os.path.relpath(BATCH_DIR, ROOT)}")
    print(f"-> {os.path.relpath(OUT_RUBRIC, ROOT)}")


if __name__ == "__main__":
    main()
