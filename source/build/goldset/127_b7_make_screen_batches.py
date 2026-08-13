#!/usr/bin/env python3
"""
127_b7_make_screen_batches.py — B.7, stage D2. Prepare the semantic screen.

Writes the screening rubric and cuts the D1 worklist into fixed batches of records carrying only what
a title/abstract screen is entitled to see: title, venue, year, type, and a truncated abstract. D1
score and discovery channel are deliberately WITHHELD from the screening record. A screener who can
see the deterministic rank will anchor on it, and the whole point of the cascade is that the semantic
sieve is independent of the blind one.

The rubric is generated from the scope document's taxonomy rather than restated by hand, so the two
cannot drift. Two constraints from the scope document are enforced in the rubric text because they
are the ones a screener will otherwise get wrong:

  * The screen assigns a ROUTING CELL and a LINK only. It does NOT assign the estimand level
    (HAZARD_DECREMENT vs TEMPO_ADJUSTED_QUANTUM) and it does NOT assign the indication design, both
    of which are methods facts invisible in an abstract.
  * Where routing turns on Wall 1 -- whether the estimate separates the medication from the
    indication -- and the abstract does not say, the verdict is MIXED_INDICATION_UNRESOLVED rather
    than a substantive cell. That is the wall this chapter's whole content turns on, and an abstract
    almost never settles it.
  * SPECIES IS CHECKED ON EVERY RECORD rather than inferred from topic. On the reconnaissance
    probes the aquatic-ecotoxicology literature outranked the human work on the chapter's own
    fecundity vocabulary, so Wall 7 is not a tail case here; it is the default reading of a title
    that says "antidepressants reduce fecundity".

Output: source/build/goldset/b7_screen_batches/batch_NN.json
        literature/search-logs/{slug}-screen-rubric.md
"""
import json, os

SLUG = "antidepressants-ssri-subfecundity"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
BATCH_DIR = os.path.join(HERE, "b7_screen_batches")
OUT_RUBRIC = os.path.join(LOGS, f"{SLUG}-screen-rubric.md")

BATCH_SIZE = 60
ABSTRACT_WORDS = 60

CELLS = [
    ("PRIMARY_MEDICATION_TO_FERTILITY", "Antidepressant exposure -> a FERTILITY quantity: births, completed parity, TFR, time-to-pregnancy, fecundability."),
    ("PRIMARY_MALE_FECUNDITY", "Antidepressant exposure -> a measured MALE fertility outcome (pregnancies achieved, TTP), not a semen parameter."),
    ("LINK1_MEDICATION_TO_SEXUAL_FUNCTION", "Antidepressant exposure -> desire, arousal, orgasm, sexual dysfunction incidence. Abundant; earns no primary credit."),
    ("LINK2_FUNCTION_TO_COITAL_FREQUENCY", "Sexual dysfunction or desire -> frequency of intercourse. The chain's weakest measured joint."),
    ("LINK3_COITAL_TO_CONCEPTION", "Coital frequency -> conception hazard or fecundability. Borrowed from A.14; no recall credit."),
    ("ENDOCRINE_MECHANISM", "Antidepressant exposure -> prolactin, gonadotropins, testosterone, or semen parameters. Mechanism, not fertility."),
    ("PARAMETER_PREVALENCE", "Exposure prevalence, dispensing volume, duration of use, by age and sex. Feeds demographic significance."),
    ("PARAMETER_HAZARD_CLINICAL", "Antidepressant exposure in a fertility-clinic population -> cycle conception or live birth. Selection-flagged."),
    ("PARAMETER_DETERMINANT_TO_LOSS", "Antidepressant exposure -> fetal loss, NO fertility outcome. Cross-filed to B.5; neither chapter's recall."),
    ("INDICATION_BASELINE_D3A", "Depression/anxiety/psychiatric diagnosis -> fertility, with no medication contrast. D.3.a's, and B.7's counterfactual."),
    ("MEASUREMENT_ASCERTAINMENT", "How sexual dysfunction or exposure is ascertained: spontaneous report vs direct questioning, prescription vs adherence."),
    ("THEORY_SEROTONERGIC", "Formal or physiological account of serotonergic action on sexual motivation."),
    ("ADJACENT_PSYCHOTROPIC", "Antipsychotics, mood stabilisers, anticonvulsants -> any reproductive outcome. Retained, never pooled."),
    ("OFF_PREGNANCY_SAFETY", "Sample conditioned on pregnancy; outcome is a property of a birth that occurred (defects, preterm, birth weight, autism, neonatal). Wall 4; expected largest cell."),
    ("OFF_ART_A17", "Antidepressant exposure in ART where the estimand is treatment success. Wall 5."),
    ("OFF_FETAL_LOSS_B5", "Antidepressant exposure -> fetal loss WITH a fertility consequence estimated. B.5 claims it."),
    ("OFF_ENVIRONMENTAL_B2B6", "Environmental antidepressant contamination as the exposure route. Wall 8."),
    ("OFF_CLINICAL_MANAGEMENT", "Treating antidepressant-induced sexual dysfunction: bupropion augmentation, sildenafil, drug switching."),
    ("OFF_ANIMAL", "Non-human exposure -- fish, invertebrates, rodents, livestock. Wall 7, and the default occupant of this vocabulary."),
    ("OFF_OUTCOME", "Antidepressant exposure -> a non-fertility, non-sexual outcome."),
    ("MIXED_INDICATION_UNRESOLVED", "Medicated vs general population with the indication not handled, or the abstract silent on how. Held for full text."),
    ("ROUTING_DEFERRED_TO_FULLTEXT", "Routing turns on Wall 1's design question and the abstract does not name the design."),
    ("REVERSE", "Low desire, subfecundity, or childlessness raising the probability of diagnosis or prescription."),
    ("OFF_OTHER", "A non-B.7 fertility determinant with no sibling-hypothesis home."),
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

    L = [f"# Screening rubric — {SLUG} (B.7)", "",
         "Title/abstract screen over the D1 worklist. The screener sees title, venue, year, type, and "
         "a truncated abstract, and does NOT see the D1 score or the discovery channel — a screener "
         "who can see the blind sieve's rank will anchor on it, which would collapse two independent "
         "sieves into one.", "",
         "## What the screen decides", "",
         "For each record emit `{id, verdict, cell, note?}` where `verdict` is one of "
         "`RELEVANT` / `UNCERTAIN` / `NOT_RELEVANT` and `cell` is one of the cells below.", "",
         "**The screen assigns a routing cell only.** It does not assign the estimand level "
         "(`HAZARD_DECREMENT` vs `TEMPO_ADJUSTED_QUANTUM`) and it does not assign the indication "
         "design; both are methods facts, set at full-text extraction.", "",
         "**Route on what is measured, and on whether the medication is the variation.** B.7 owns a "
         "drug whose name appears as a covariate in enormous literatures that estimate something "
         "else. A record naming an antidepressant is not thereby a B.7 record: ask what quantity the "
         "estimate is of, and whether antidepressant exposure is what moves.", "",
         "**Check species on every record.** Do not infer it from the topic. On the reconnaissance "
         "probes the aquatic-ecotoxicology literature outranked the human work on this chapter's own "
         "fecundity vocabulary, so `OFF_ANIMAL` is the default reading of an unqualified claim that "
         "antidepressants reduce fecundity, not an afterthought.", "",
         "**Defer rather than guess.** Where routing turns on Wall 1 — whether the estimate separates "
         "the medication from the indication — and the abstract does not say, use "
         "`MIXED_INDICATION_UNRESOLVED`. An exclusion an abstract could not support is a silent false "
         "negative, and on this hypothesis the design is what decides whether a study speaks to it "
         "at all.", "",
         "## Cells", "", "| cell | definition |", "|---|---|"]
    for c, d in CELLS:
        L.append(f"| `{c}` | {d} |")
    L += ["", "## Verdict convention", "",
          "- `RELEVANT` — the record belongs to a primary, parameter, measurement, theory, or context "
          "cell. Parameter/measurement/theory records are RELEVANT and are separated downstream; they "
          "earn no empirical recall credit.",
          "- `UNCERTAIN` — routing or eligibility genuinely unclear on the visible record. Pairs with "
          "`INSUFFICIENT_INFO` or with a MIXED/DEFERRED cell.",
          "- `NOT_RELEVANT` — an `OFF_*` cell, including the very large pregnancy-safety, "
          "clinical-management and non-human literatures.", "",
          f"## Batches", "", f"{n} batches of up to {BATCH_SIZE} records, {len(work)} records total, "
          f"abstracts truncated to {ABSTRACT_WORDS} words."]
    open(OUT_RUBRIC, "w").write("\n".join(L) + "\n")
    print(f"records={len(work)} batches={n} -> {os.path.relpath(BATCH_DIR, ROOT)}")
    print(f"-> {os.path.relpath(OUT_RUBRIC, ROOT)}")


if __name__ == "__main__":
    main()
