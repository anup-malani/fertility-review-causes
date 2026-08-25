#!/usr/bin/env python3
"""
190_a17_make_screen_batches.py — A.17, stage D2. Prepare the semantic screen.

Inherits `175_a24_make_screen_batches.py`. Writes the screening rubric and cuts the D1 worklist into
fixed batches carrying only what a title/abstract screen is entitled to see: title, venue, year,
type, and a truncated abstract.

WITHHELD FROM THE SCREENING RECORD, deliberately:
  * the D1 score and rank — a screener who can see the blind sieve's output anchors on it, which
    collapses two independent sieves into one;
  * the `worklist_reason`. A record told "this arrived through the arm-2 bypass" invites a screener
    to read a policy design into an abstract that states none. The bypass is a retrieval decision;
    whether the record carries the design is what the screen is being asked;
  * D1's `access_hits`, `count_hits`, `popfert_hits`, `ident_hits` and the wall hit-lists, so the
    screener's `arm` and `outcome_type` are INDEPENDENT readings that assembly can cross-check.

`arm` IS THE FIELD THIS SCREEN EXISTS FOR. A.17's scope found the hypothesis has two arms answering
different questions — arm 1 COUNTS ART births (an upper bound on the claim) and arm 2 ESTIMATES the
response to access (a lower one) — and ruled they must never be pooled. The scope also declared the
split invisible at title/abstract, because it is usually decided in the methods section.

**A4 contradicted that in one direction and the rubric carries the correction.** Identification
vocabulary runs 1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones — a 4x prior — while counting
vocabulary is flat (3.9% against 6.0%). So a record carrying identification language is
disproportionately arm 2, and a record lacking it says nothing at all. `cannot_tell` is therefore a
first-class value, not a failure: the SHARE of records landing there is the measurement that decides
how much of the routing has to happen at full text, and suppressing it would convert a measurement
into an assumption.

`preservation_indication` IS AN INDEPENDENT RE-READ OF WALL 5. A4 measured the preservation
population by term-matching: 76% oncological, 5% elective, 17% naming neither. That is a vocabulary
measurement of a wall the scope had declared unenforceable, and it narrowed the declaration to the
17%. Having the screener name the indication independently is what turns the term count into a
routing decision — and the disagreements between the two are Wall 5's working set rather than errors.

THE NO-ABSTRACT BUCKET IS NOT A NEGATIVE VERDICT. 33% of the frame carries a title only. A screener
who returns `NOT_RELEVANT` on a title-only record has recorded "not visible" as "not relevant", which
is the refusals-read-as-zeros failure in its third costume. Those records take `INSUFFICIENT_INFO`
with `UNCERTAIN` unless the TITLE ALONE is decisive — and a title often is, in both directions.

Output: source/build/goldset/a17_screen_batches/batch_NN.json
        literature/search-logs/{slug}-screen-rubric.md
"""
import json, os

SLUG = "art-access-fertility-recovery"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
BATCH_DIR = os.path.join(HERE, "a17_screen_batches")
OUT_RUBRIC = os.path.join(LOGS, f"{SLUG}-screen-rubric.md")

BATCH_SIZE = 60
ABSTRACT_WORDS = 70

CELLS = [
    ("P1_MANDATE",
     "A change in ART ACCESS — insurance mandate, public funding, reimbursement reform, subsidy, "
     "price change, legal eligibility — estimated against a POPULATION fertility outcome: births, "
     "birth rates, first births, parity progression, completed fertility. **This is the chapter's "
     "only identified evidence and it is 133 records in 7,313.** Errs toward inclusion."),
    ("P2_AVAILABILITY",
     "ART SUPPLY rather than price: clinic entry or closure, distance to a clinic, provider density, "
     "legal availability, cross-border access — against a population fertility outcome. Same "
     "estimand as P1 through a different instrument. The recon probe found this cell thin; if it "
     "stays thin that is a finding about the literature."),
    ("P3_ART_SHARE",
     "ART utilisation or ART-conceived births MEASURED and expressed as a share of all births, or as "
     "a contribution to TFR / completed fertility / parity transitions. **Arm 1's core.** This is a "
     "COUNT, not an estimate — route it here even when the paper's own language calls it an effect."),
    ("P4_POSTPONEMENT_RECOVERY",
     "A model, simulation or projection of what postponement costs and how much ART recovers: "
     "involuntary childlessness, completed-fertility shortfall, age-at-start tables. Leridon and "
     "Habbema's literature. Arm 1, and the source of the chapter's recovery fraction."),
    ("P5_ELECTIVE_PRESERVATION",
     "ELECTIVE oocyte cryopreservation / social egg freezing — availability, employer coverage, "
     "uptake — against later births or completed fertility. **PI call 2's cell.** A4 counted ~49 "
     "candidates in the whole frame, so this cell will likely come back near-empty; read it in full "
     "so that emptiness can be reported as a finding rather than as an absence of effort."),
    ("P6_INDUCED_POSTPONEMENT",
     "Does ART's AVAILABILITY (or beliefs about its success) induce the postponement it then "
     "repairs? The upper-bound channel. Includes the fertility-awareness literature showing adults "
     "overestimate ART success. **Flag in the note whether the record measures the BELIEF or the "
     "BEHAVIOUR** — the scope found the belief side measured and the behaviour side not, and the "
     "chapter's verdict depends on that distinction holding."),
    ("EXPOSURE_SERIES",
     "A registry, surveillance or monitoring report supplying ART cycles, ART births or utilisation "
     "as a SERIES: ICMART, ESHRE/EIM, CDC/SART, ANZARD, national registers. Not an estimate and not "
     "an error — the demographic-significance stage cannot run without these."),
    ("ROUTE_A12_MULTIPLES",
     "The estimated outcome is the MULTIPLE-BIRTH RATE per delivery. A.12's, by the scope-freeze "
     "ruling. **Route by OUTCOME, not by topic:** an insurance-mandate paper whose outcome is the "
     "multiple-birth rate is A.12's; the same paper's deliveries or births results are A.17's. A "
     "paper reporting both goes here AND is flagged `both_arms_present` in the note — Buckles 2012 "
     "is exactly this case and both chapters extract it on different rows."),
    ("ROUTE_A15_POSTPONEMENT",
     "About why age at first birth ROSE — the causes of postponement itself. A.15's. A.17 takes "
     "postponement as given and asks what ART recovers from it."),
    ("ROUTE_B_SUBFECUNDITY",
     "About why infertility or subfecundity rose: sperm-count decline, endocrine disruptors, "
     "obesity, antidepressants. B.2 / B.4 / B.6 / B.7's. A.17 begins after the diagnosis."),
    ("OFF_CLINICAL",
     "Outcome is a per-cycle or per-transfer probability: live birth rate per cycle, clinical "
     "pregnancy rate, implantation, stimulation protocol, embryo selection, culture media. Wall 1, "
     "and the largest decoy in the chapter at 204,210 records — measured at 0.1% on-estimand."),
    ("OFF_SAFETY",
     "Outcome is offspring or maternal safety: birth defects, preterm, birth weight, neonatal or "
     "perinatal morbidity, OHSS, maternal complications. Wall 2. A4 measured this cloud at 33% loose "
     "outcome vocabulary and 0% strict — it says 'birth' constantly and a population quantity never."),
    ("OFF_ONCOFERTILITY",
     "Fertility preservation for a MEDICAL indication: before chemotherapy, radiotherapy or other "
     "gonadotoxic treatment. Wall 5's enforceable majority — A4 measured 76% of the preservation "
     "population naming an oncological indication outright."),
    ("OFF_COST_EFFECTIVENESS",
     "Payer-perspective economics with NO birth count: cost per live birth, budget impact, QALYs, "
     "willingness to pay. Wall 6. A cost study that ALSO reports births belongs in P1 or P3."),
    ("OFF_OTHER",
     "No A.17 content and no sibling-hypothesis home."),
    ("INSUFFICIENT_INFO",
     "Cannot be routed on the visible record. Pairs only with UNCERTAIN. **Expected to be common: a "
     "third of this frame carries a title only.**"),
]

ARMS = [
    ("arm2_estimate",
     "The record ESTIMATES a response to a change in access, availability or price. Identification "
     "language — difference-in-differences, natural experiment, IV, event study, policy reform, "
     "staggered adoption — is a strong positive signal for this value."),
    ("arm1_counting",
     "The record COUNTS or PROJECTS: a share of births, a contribution to TFR, a registry "
     "tabulation, a simulation of what ART recovers. No counterfactual is estimated from variation."),
    ("both",
     "The record does both — typically a policy paper that also tabulates ART's share of births."),
    ("neither",
     "Not an A.17 quantity at all (most decoy records)."),
    ("cannot_tell",
     "**A first-class value, not a failure.** The abstract does not reveal whether a counterfactual "
     "was estimated or a share tabulated. The SHARE of records landing here is the measurement that "
     "decides how much routing must happen at full text. Use it freely and honestly."),
]

OUTCOME_TYPES = [
    ("population_fertility", "Births, birth rates, TFR, completed fertility, parity progression, childlessness at the population or cohort level."),
    ("per_cycle_clinical", "Live birth rate per cycle or transfer, pregnancy rate, implantation rate — a treatment success probability."),
    ("multiple_birth_rate", "The multiple-birth or twinning rate per delivery. A.12's outcome."),
    ("utilisation_only", "Treatment uptake, cycles performed, access or utilisation rates, with no birth outcome reported."),
    ("postponement", "Age at first birth, delayed childbearing, timing of the reproductive window."),
    ("belief_or_attitude", "Awareness, knowledge, expectations, intentions, attitudes — what people think, not what they do."),
    ("safety", "Offspring or maternal health outcomes."),
    ("cost", "Money: expenditure, cost per birth, budget impact."),
    ("other", "None of the above."),
    ("none_visible", "The record does not state an outcome. Pairs with INSUFFICIENT_INFO."),
]

PRESERVATION = [
    ("onco", "A medical indication is named: cancer, chemotherapy, radiotherapy, gonadotoxic treatment."),
    ("elective", "An elective / social / non-medical indication is named, including employer benefits."),
    ("neither", "**Wall 5's residue.** A preservation paper naming NO indication. A4 measured this at 17% of the preservation population by vocabulary; this field is the independent re-read."),
    ("n_a", "Not a fertility-preservation record."),
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

    n_abs = sum(1 for r in work if r.get("abstract"))
    by_reason = {}
    for r in work:
        by_reason[r["worklist_reason"]] = by_reason.get(r["worklist_reason"], 0) + 1

    L = [f"# Screening rubric — {SLUG} (A.17)", "",
         f"Title/abstract screen over the D1 worklist: **{len(work):,} records in {n} batches of "
         f"{BATCH_SIZE}**. The screener sees title, venue, year, type and up to "
         f"{ABSTRACT_WORDS} words of abstract, and does NOT see the D1 score or rank, the "
         "`worklist_reason`, or D1's term-hit lists.", "",
         f"**{n_abs:,} of {len(work):,} worklist records carry an abstract "
         f"({n_abs / max(len(work), 1):.0%}).** The remainder are title-only — see the standing "
         "instruction on `INSUFFICIENT_INFO`.", "",
         "## What the screen decides", "",
         "For each record emit `{id, verdict, cell, arm, outcome_type, preservation_indication, "
         "note?}` where `verdict` is `RELEVANT` / `UNCERTAIN` / `NOT_RELEVANT` and the other four "
         "are drawn from the tables below.", "",
         "## Standing instructions, each tied to something measured", "",
         "**Never pool the arms — that is what the `arm` field is for.** Arm 1 COUNTS ART births and "
         "is an UPPER BOUND on this chapter's claim; arm 2 ESTIMATES the response to access and is a "
         "lower one. They are not two estimates of one parameter, so a screen that merges them "
         "destroys the distinction the chapter turns on. A4 found identification vocabulary running "
         "**1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones** — a real 4x prior for arm 2, "
         "and a thin one, since 94% of arm 2's own neighbourhood carries none of it. So "
         "identification language is evidence FOR `arm2_estimate`; its absence is evidence for "
         "nothing.", "",
         "**`cannot_tell` is a first-class value and its share is a result.** The scope declared the "
         "arm split invisible at title/abstract. A4 said partly visible. This screen is the "
         "tiebreak, and it only works if `cannot_tell` is used honestly rather than resolved by "
         "guessing. A high share means the routing stays a full-text decision and the chapter says "
         "so; a low share means the screen can carry part of the load.", "",
         "**An ART share of births is a COUNT, not an effect — even when the paper calls it one.** "
         "The single most consequential routing error available here is putting a tabulated share "
         "into `P1_MANDATE` because its abstract says ART 'increased fertility by X%'. That number "
         "assumes every ART birth is counterfactually additional, which is precisely the assumption "
         "the chapter exists to test. It is `P3_ART_SHARE` with `arm1_counting`.", "",
         "**Route Wall 3 by OUTCOME, not by topic.** An insurance-mandate paper whose estimated "
         "outcome is the MULTIPLE-BIRTH RATE is A.12's, however much it looks like arm 2. The same "
         "paper's births or deliveries results are A.17's. When both appear, use "
         "`ROUTE_A12_MULTIPLES` and write `both_arms_present` in the note: the two chapters extract "
         "such a paper on different rows and their contributions still sum without double-counting.", "",
         "**Wall 5 is a screen rule with a residue, not an unenforceable wall.** The scope declared "
         "it unenforceable; A4 measured the preservation population at **76% naming an oncological "
         "indication, 5% elective, 17% naming neither**, so it IS enforceable for five records in "
         "six. `preservation_indication` is your INDEPENDENT re-read of that split. Do not infer an "
         "elective indication from the absence of an oncological one — 'neither' is the answer when "
         "neither is named, and that residue is the working set.", "",
         "**The sign is not given by the theory.** v5 asserts ART RAISES TFR relative to the "
         "counterfactual. The recent accounting literature in this frame includes titles suggesting "
         "the opposite. A record finding ART's contribution negligible, or finding a mandate had no "
         "effect on births, is `P3_ART_SHARE` or `P1_MANDATE` exactly like one finding a large "
         "effect. Screening on the expected direction would manufacture the result.", "",
         "**A title-only record is not a negative.** A third of this frame carries no abstract. "
         "`NOT_RELEVANT` on such a record records *not visible* as *not relevant* — the same failure "
         "as reading a refused request as a zero. Use `INSUFFICIENT_INFO` + `UNCERTAIN` unless the "
         "TITLE ALONE is decisive, which it often is in both directions.", "",
         "## Worklist composition", "", "| reason | n |", "|---|---|"]
    for k, v in sorted(by_reason.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | {v:,} |")
    L += ["",
          "Bypass records are interleaved by rank order within their group; the screener cannot tell "
          "a bypass record from a budget-slice one, which is the point.", "",
          "## Cells", "", "| cell | definition |", "|---|---|"]
    for k, v in CELLS:
        L.append(f"| `{k}` | {v} |")
    L += ["", "## `arm` — the routing field", "", "| value | definition |", "|---|---|"]
    for k, v in ARMS:
        L.append(f"| `{k}` | {v} |")
    L += ["", "## `outcome_type`", "", "| value | definition |", "|---|---|"]
    for k, v in OUTCOME_TYPES:
        L.append(f"| `{k}` | {v} |")
    L += ["", "## `preservation_indication`", "", "| value | definition |", "|---|---|"]
    for k, v in PRESERVATION:
        L.append(f"| `{k}` | {v} |")
    L += ["", "## Verdict", "",
          "- `RELEVANT` — belongs in an A.17 cell (`P1`-`P6` or `EXPOSURE_SERIES`).",
          "- `UNCERTAIN` — plausibly A.17 but the record does not settle it; pairs with "
          "`INSUFFICIENT_INFO` or with a cell plus `cannot_tell`.",
          "- `NOT_RELEVANT` — a wall cell or a route to a sibling hypothesis. **A `ROUTE_*` record "
          "is NOT_RELEVANT for A.17 and is not discarded** — the routing is the deliverable.", ""]
    open(OUT_RUBRIC, "w").write("\n".join(L) + "\n")
    print(f"wrote {n} batches of {BATCH_SIZE} to {os.path.relpath(BATCH_DIR, ROOT)}")
    print(f"-> {os.path.relpath(OUT_RUBRIC, ROOT)}")
    print("worklist composition:", by_reason)


if __name__ == "__main__":
    main()
