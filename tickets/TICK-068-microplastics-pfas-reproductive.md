# TICK-068: B.6. Microplastics and PFAS in Reproductive Tissues
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `microplastics-pfas-reproductive` — HYPOTHESES-v5.md §B.6
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/microplastics-pfas-reproductive-*, extraction/microplastics-pfas-reproductive-*, output/chapters/microplastics-pfas-reproductive-{pfas,microplastics}.md, source/build/goldset/13*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [x] 3. Literature search and AI screening, both phases (§5.1) — **done 2026-08-14, 920/920 screened**
  - [x] 3a. A3 cold-start anchors sourced and gated — 32/32 verified
  - [x] 3b. A4 Tier A / Tier B citation frame — 14,561 records, 0 failed requests
  - [x] 3c. D1 deterministic rank and screening cutoff — worklist 920
  - [x] 3d. D2/E1 semantic screen and assembly — 433 RELEVANT, five validations passed
- [ ] 4. RA title/abstract review — **gate worksheet ready: `extraction/microplastics-pfas-reproductive-ra-gate.csv`, 156 rows. Deliberately NOT done by me: the AI screen and the RA gate are designed as independent passes**
- [ ] 5. Full-text retrieval — **119/239 readable (50%) after two automated passes; extraction proceeds against what is held**
  - [ ] 5a. Library pass on the residual 118 — needs Zotero + UChicago proxy. List: `literature/search-logs/microplastics-pfas-reproductive-library-wantlist.md`, ordered by value, safe to stop partway. Job A first (12 records), PFAS before microplastics
- [x] 6. Full-text screen — **done 2026-08-14 on the 53 held primary/input documents (`143` locates the methods facts, `144` codes them). RA spot-check outstanding**
- [x] 7. Extraction — **first pass done: `extraction/microplastics-pfas-reproductive-effects.csv`, 17 rows. RA 10% verification outstanding; 5 rows need PDF-quality re-extraction**
- [x] 8. Risk-of-bias assessment — **first pass done: `extraction/microplastics-pfas-reproductive-risk-of-bias.csv`, 10 domain ratings**
- [x] 9. Synthesis — **narrative both times; neither family meets PROTOCOL §5.9's three-estimate bar**
- [x] 10. Demographic significance — **PFAS not significant (wrong-signed slope); microplastics not computable**
- [x] 11. GRADE — **both families Very low, for opposite reasons. §5.11 three-rater panel NOT run and not simulated; outstanding**
- [x] 12. Chapter drafts on the §6 template — **two chapters drafted 2026-08-14** (Call 1):
  - [x] 12a. `output/chapters/microplastics-pfas-reproductive-pfas.md` (2,515 words, all 11 sections)
  - [x] 12b. `output/chapters/microplastics-pfas-reproductive-microplastics.md` (2,043 words, all 11 sections)
- [ ] 13. RA lay-readability check, both chapters
- [ ] 14. PI review and sign-off, both chapters

## Log

**2026-08-14 — opened (Shravan).** Scripts for this hypothesis start at
`source/build/goldset/132_b6_*`. 131 is the highest number in use anywhere — it is on the
unmerged `066-antidepressants-ssri-subfecundity` branch, and 115 is on `062-postmaterialism-…`,
which exists only locally and is invisible from `origin`. Numbering above `main` alone would have
collided a third time.

**2026-08-14 — stage 2 done (Shravan): search strategy and scope drafted.**
`literature/search-logs/microplastics-pfas-reproductive-search-scope.md`, built on the B.7 template,
against two live OpenAlex passes (`132_b6_recon_probe.py`, 72 probes; `133_b6_anchor_retry.py`, 20
probes; **zero failed requests in both**, so the zero counts are absences and not refusals). Nine
walls specified, five scope calls raised with recommendations. Three findings drive the design:

1. **B.6 bundles two hypotheses with opposite profiles.** PFAS has real human fertility epidemiology
   (time-to-pregnancy n = 127, two prior meta-analyses) and a *falling* legacy exposure series —
   NHANES reports PFOS and PFHxS declining after production was discontinued. Microplastics has the
   new tissue-detection literature and a *rising* series, but essentially no human fertility
   epidemiology. v5's note that "the exposure is structurally rising" is false for the half that
   carries the evidence. Call 1 asks for per-family verdicts.
2. **No quasi-experimental estimate of either exposure on a fertility quantity exists.** The only
   natural experiment found (Waterfield et al. 2020, a difference-in-differences on a Minnesota water
   filtration plant) has birth weight and preterm birth as outcomes, so Wall 2 routes it out. The
   GRADE ceiling is set before the search runs, on design rather than volume.
3. **Three of v5's four seminal citations do not resolve as written**, including one that is a
   phthalate paper — i.e. on the B.2 side of the wall that defines B.6. Detailed in Call 4 for
   TICK-001, with a recommendation to re-verify the other v5-era entries on the same gates.

**2026-08-14 — Call 1 decided; walls frozen.** B.6 stays **one hypothesis, one entry in
`HYPOTHESES-v5.md`, one ticket, one search**, and produces **two chapters** — one per chemical
family. The split lands at extraction, on `CHEMICAL_FAMILY`; everything upstream (walls, screen,
anchors, PRISMA identification and screening counts) is shared, and stages 9–14 run twice. Promoting
the families to B.6.a/B.6.b in the hypothesis list was considered and **not** done: the taxonomy is
TICK-001's to change, and renumbering the master list propagates into every in-flight branch's
`HYPOTHESES-v5.md §X` reference. The registry question goes to the PI for v6 alongside the Call 4
citation corrections, since both edit the same entry. With Call 1 answered, **the nine walls are
frozen**; Calls 2, 3 and 5 remain open and none of them blocks the search.

**2026-08-14 — Calls 2, 3 and 5 decided; A3 anchors done (32/32 verified).** Call 2: two-track
synthesis on `PARITY_HANDLING`, with the gap between tracks reported as a quantity of interest.
Call 3: Waterfield et al. (2020) stays excluded from synthesis but is **extracted and reported as a
flagged aside** under a new `ASIDE_EXTRACTED` disposition — a routed-out record carrying stronger
identification than anything included, reported with its estimand mismatch stated in the same
sentence as its estimate, and barred from every pooled quantity and recall denominator. Candidate
rule for PROTOCOL §5.9, flagged not added. Call 5: detection rated as exposure, never as effect.

A3 (`134_b6_cold_start_anchors.py`) resolved 32 anchors, all verified live, across 13 estimand cells
with one routing decoy per wall. Two defects in the **inherited** B.7 resolver surfaced, both found
by testing the new gate rather than by reading:

1. **Three shadow patterns were dead code.** They are matched against `norm()`-stripped titles, which
   remove all punctuation, so `^re\s*:`, `^corrections?\s+(to|for)` and the `letter to the editor`
   variant could never match the live forms `Re: X`, `Correction: X`, `Letter to the editor, X`. The
   miss surfaced because "Correction: The Minderoo-Monaco Commission…" scored 120, **tied with the
   article of record**, and was kept out of the anchor slot only by the tie-break. Fixed; shadow
   catches went 7 → 12 with one integrity flag. A start-up self-test on eight real pairs now aborts
   the run if the gate under-refuses. **`124_b7_cold_start_anchors.py` has the same three holes and
   its docstring claims a "Re:" catch it cannot have made** — needs fixing on the 066 branch.
2. **The duplicate-record gate's motivating case was misdiagnosed, and the gate could have caused
   harm.** `aogh.4056` and `aogh.4083` share title, year, volume and venue but are *different works* —
   48 authors under Landrigan versus a single-author companion piece by Maria Neira — and the author
   gate separates them correctly on its own. Since `author_match` returns None (passes) when a record
   has no author metadata, a bare title+year+venue rule would have silently demoted legitimately
   distinct same-title works. Demotion now requires positive author agreement. The gate has **zero
   confirmed catches** and is retained only as an unvalidated safeguard.

**2026-08-14 — A4 Tier A/B frame built (`135_b6_tier_ab_frame.py`).** 14,561 deduplicated Tier B
records from 32 seeds, **zero failed requests**, 60% carrying an abstract. Three changes on B.7's
builder: a second per-seed diagnostic (`animal >=`, a lower bound on the non-human share, because
Wall 5 is this chapter's biggest precision threat and it deserves a number); review seeds
forward-cited but **excluded from the empirical count**, which drops the causal recall denominator
from 9 to **6** — filing the three channel-1 reviews under a primary cell was right for the estimand
and wrong for the denominator; and the forward cap raised 1200 → 2000 for B.6's much larger clouds.

Three findings worth carrying into A5/A6:

1. **The routing decoys are the richest fertility-dense channels in the frame, by a wide margin.**
   The Wall 7 decoy (Levine 2017, sperm-count trend) runs **77% on-topic** — the highest of any seed —
   and the Wall 1 mixture decoy (Bellavia 2022) **51%**, against 22–47% for the PFAS primary seeds.
   1,849 Tier B records (13%) depend on a decoy seed alone and **would not exist under the inherited
   never-forward-seed-a-decoy rule.** This is the strongest confirmation yet of the D.2.d correction.
2. **The two families separate cleanly on the diagnostic.** PFAS primary seeds: 22–47% on-topic.
   Microplastics detection seeds: **2–19%**, with Plasticenta at 2.6%, Leslie at 2.5% and Schwabl at
   2.4%. The MP half of the chapter has no fertility literature to find, measured rather than
   asserted, and this is independent evidence for the Call 1 split.
3. **Wall 5's floor is 6–42% depending on seed**, highest on the oyster decoy as designed. Even the
   PFAS clouds carry 6–22% visibly non-human, so species must be checked on every record at screen.

Three seeds hit the 2,000 cap (Plasticenta, Leslie, Olsen half-life); the log now estimates the cost
at ~76 on-topic records unseen against a frame of 14,561, all three being 2.5–5% yield seeds.

**2026-08-14 — D1 rank and screening cutoff (`136_b6_d1_rank.py`).** 14,561 Tier B records, 265
version duplicates collapsed on normalised title, 14,296 distinct works ranked; worklist **920** =
top 700 by score + 0 orthogonal bypasses + **220 both-axes completeness bypasses**; 13,376
unscreened, margin score 60.

`CHEMICAL_FAMILY` is now assigned deterministically at D1, since the chapter splits on it and the
compound is the one routing call reliably visible in a title. Frame breakdown: pfas 3,550 ·
plastic 5,865 · both 50 · none 4,831. Carrying **both axes**: pfas 331 · plastic 168 · both 4 ·
none 0 — the two-family asymmetry the scope predicted, now visible in the frame itself.

Two corrections made during the run, both to my own work rather than to inherited code:

1. **The completeness bypass was family-restricted and that was incoherent.** As first written it
   screened every plastic-family both-axes record at any rank, to keep the MP half's expected null
   distinguishable from never having looked — but it left **135 both-axes PFAS records unscreened**,
   protecting the half heading for a null while under-reading the half that will carry a synthesis.
   The rule is now family-blind: every both-axes record is screened wherever it ranks.
   **`unscreened_both_axes` is now 0.**
2. **`in vitro` is a substring of `in vitro fertilization`**, so every IVF record was collecting the
   Wall 6 mechanism penalty and silently undoing the deliberately near-zero ART penalty — which
   exists for the measured reason that the ART/mixture decoy was the second most on-topic seed in the
   A4 frame. The IVF phrase is stripped before the Wall 6 table is applied, and only for that table.

Sanity check on the output: the top-ranked records are PFAS time-to-pregnancy studies, with a
**nulliparous-restricted** design at rank 4 and a preconception-measured couple-fecundability study
at rank 5 — the two designs Call 2 and the identification cautions single out as the ones that
identify. The ranker is finding what the scope said to look for.

**2026-08-14 — AI screen complete (920/920) and E1 assembly (`137`, `138`).** 433 RELEVANT, 462
NOT_RELEVANT, 25 UNCERTAIN. Tier 1 279 · tier 2 154 · tier 3 25. Primary-cell 30, fertility-input
(semen/ovarian) 70, support 302, held 56. RA gate worksheet has 156 rows.

All five validations pass: anchor recovery **4/4**; decoy containment **45/51 routed away (88%)**,
so the walls hold without swallowing the boundary cases decoys exist to supply; chemical-family
agreement between D1's deterministic tag and the blind screener **857/920 (93%)**.

**The Call 1 split is confirmed by the counts, and the direction is the surprise:**

| cell group | pfas | plastic | both |
|---|---|---|---|
| PRIMARY (a fertility quantity) | 19 | 10 | 1 |
| INPUT (semen / ovarian parameter) | 62 | 7 | 0 |

1. **The microplastics effect cell is NOT empty, and the scope document was wrong to expect it
   would be.** Ten plastic-family records carry a fertility quantity, and the screen found human MP
   studies with measured outcomes that the reconnaissance missed entirely: MP in follicular fluid
   against diminished ovarian reserve (two independent groups), MP in semen against sperm quality
   (three studies), polyethylene MP against oocyte quality in a human-and-mouse design, and a
   plastic-tableware-use exposure contrast against sperm quality. A systematic review of MP and
   *human* reproductive outcomes also exists — the recon found none. **The 2024–2026 publication
   wave is the reason; the probes ran on citation-ranked heads, which are structurally older.** The
   MP chapter will not be a pure null after all, though its evidence remains cross-sectional.
2. **The asymmetry survives, in the INPUT row rather than the PRIMARY row.** PFAS has 62 semen and
   ovarian parameter records to microplastics' 7 — a nine-to-one ratio. The two halves differ less
   in whether a fertility quantity has been estimated than in the depth of measured biology beneath
   it.
3. **`PRIMARY_HIGH_EXPOSURE` is EMPTY — zero records in 920.** Wall 9's contaminated-community and
   occupational cohorts (Ronneby, Veneto, C8, firefighters, Mid-Ohio Valley) appear ~20 times, and
   every one is either exposure characterisation or a Wall 2 pregnancy outcome. **The populations
   with the only exogenous exposure variation have never been studied for a fertility outcome.**
   That is a stronger and more specific statement of the identification problem than the scope
   document made, and it belongs in both chapters' GRADE rationale.

Two defects found and fixed, plus one taxonomy gap:

- **Shadow records inside Tier B: 10.** The A3 gate protects only the anchor set. Open-peer-review
  journals mint a separately-DOI'd record per referee report — one eLife paper occupies **six** rows
  in this frame (article, duplicate, Author Response, three Reviewer Public Reviews) and one PeerJ
  review occupies **four**. Also caught: a `RETRACTED:` record whose retracted status lives only in
  the title string. `Author Response:`, `Reviewer #N (Public Review):`, `Peer Review #N of` and
  `Comment on:` all need adding to the A3 `SHADOW_QUALIFIERS`, and D1's title-collapse should strip
  a leading qualifier before grouping.
- **I repeated the punctuation bug I had fixed hours earlier.** The shadow scan's first version used
  `^reviewer\s+#?\d+\s*\(` — a literal `(` that `norm()` deletes — and `^retractions?`, which
  misses `RETRACTED:`. Detections went 6 → 10 once fixed. Knowing the bug class did not prevent
  rewriting it; running the gate against a case it should catch did.
- **Taxonomy gap:** B.6's cell list has no adult reproductive-endocrine parameter cell. B.7 had
  `ENDOCRINE_MECHANISM` and it was not carried across, so serum testosterone and sex-hormone records
  in adults were routed to the nearest sex-specific cell. Three records affected; add the cell before
  extraction.

**2026-08-14 — stage 5 wantlist and OA ceiling (`139`).** Four retrieval jobs rather than B.7's
three. The fertility-INPUT cells (semen, ovarian) get their own job because that is where this
chapter's measured biology actually is — 70 records against 30 in the primary cells — and folding
them into a generic "support" bucket, as B.7's structure would, would mis-describe the evidence base.

OA status checked live **before** the fetch, per the B.1 lesson:

| job | records | open | rate |
|---|---|---|---|
| A — primary (a fertility quantity) | 30 | 20 | 67% |
| A2 — input (semen, ovarian) | 70 | 59 | 84% |
| B — held for a routing question | 56 | 39 | 70% |
| C — parameter, pharmacokinetic, measurement | 84 | 70 | 83% |

**This chapter is not retrieval-bound.** Against B.1's automated ceiling of 20/95 (21%), which has
kept its pooled estimate resting on five studies since July, a 67% ceiling on the primary cell means
the library sub-ticket is a completeness measure rather than a precondition. Zero OA checks failed,
so every "closed" here is a real closure and not an unconfirmed request.

**The selection test.** Because this chapter's design is a comparison between its two halves, a
retrieval process that reaches one half more completely biases the comparison itself and not merely
the level — and the microplastics literature, being newer, is more often gold-OA, which is precisely
the condition for that bias. Measured over the causal evidence base (A + A2): **pfas 62/81 (77%),
plastic 15/17 (88%)**. An 11-point gap in the direction predicted. Not large enough to invalidate the
comparison, large enough that the limitations paragraph must quote it, and a reason to prioritise the
closed PFAS records in any library request.

Job C is selected by RULE from the screen notes rather than hand-listed, so the set regenerates if
the screen is revised — 84 records covering the Call 2 reverse-causation evidence (`r`), excretion
and half-life pharmacokinetics (`k`), the exposure series the demographic-significance computation
multiplies (`x`), measurement and design (`m`), and outcome-trend context (`t`).

**2026-08-14 — stage 5 fetch complete (`140`, `141`, `142`). 119/239 readable (50%).**

Pass 1 (`140`, publisher + repository routes) returned **92/239**, thirty-nine points below the OA
ceiling `139` had measured. **96 records OpenAlex calls OPEN failed to fetch**, splitting 40
"Europe PMC hit but not OA" and 38 "publisher interstitial, not a PDF". The ceiling was a forecast;
this is what landed.

**Pass 2 (`141`) diagnosed the first group and recovered 27 of them.** Those records are
author-manuscript deposits in PubMed Central — `isOpenAccess: N` but `inEPMC: Y` and `hasPDF: Y` —
so Europe PMC's `fullTextXML` 404s while NCBI's `efetch` serves the full JATS body. Verified live on
`PMC5131715` and `PMC10234267` before writing the script: both 404 at EPMC, both return >110 KB with
a 33k-character `<body>` from efetch.

**The inherited route ladder had a conceptual bug worth naming: it gated on `isOpenAccess`, which
conflates OPEN ACCESS (a licence fact) with RETRIEVABLE (an access fact).** For NIH-funded work the
two routinely come apart. `130_b7_fetch_oa.py` has the same gate and would recover similarly on B.7.

**The selection test, measured rather than forecast.** The `139` ceiling predicted an 11-point family
gap (PFAS 77%, plastic 88%). Realised retrieval after pass 1 was **PFAS 38%, plastic 59% — a 21-point
gap, twice the forecast**. The efetch recovery pulled PFAS to **51% against plastic 59%**, closing it
to 8 points, because author-manuscript deposits are concentrated in the NIH-funded PFAS cohorts. The
fix worked against the bias rather than with it, which was the reason for trying it first.

| job | readable | rate |
|---|---|---|
| A — primary cell | 15/29 | 52% |
| A2 — input (semen, ovarian) | 38/70 | 54% |
| B — held for routing | 26/56 | 46% |
| C — parameter and measurement | 40/84 | 48% |

**The residual 118 stays inside this ticket** as criterion 5a rather than becoming a sub-ticket.
`tickets/README.md` allows a retrieval sub-ticket when the stage blocks on library access; here it
does not block — 50% readable including 15 of 29 primary-cell records is enough to run extraction,
so a separate ticket would add tracking overhead without unblocking anything. If a human never gets
to 5a, the chapter still reports; it reports with a stated retrieval rate.

The list is `literature/search-logs/microplastics-pfas-reproductive-library-wantlist.md`: 73
route-blocked (open, publisher refuses scripts — often just a browser click, no proxy needed) and 45
genuinely closed. Ordered by retrieval value with the PFAS half first, so procurement shrinks the
family gap rather than entrenching it. Two shadow/duplicate records are explicitly excluded — asking
a human to fetch a peer-review artefact wastes the scarcest resource in the pipeline.

Highest-value single record: **`Serum perfluoroalkyl acids and time to pregnancy in nulliparous
women`** (closed) — the parity-handled design the Call 2 restricted track is built on.

**2026-08-14 — stages 6-8 first pass (`143`, `144`). 17 effect rows, 10 risk-of-bias ratings.**

`143` probes the 53 held primary/input documents for the four methods facts the screen could not
assign, quoting the passage where each is stated, so the hand-coding has located evidence behind it
rather than recall. Coverage: `PARITY_HANDLING` discussed in 27/53 (51%), enough for a restricted
track to exist.

**THE CENTRAL RESULT — the two tracks disagree, and both cohorts that tested it say so.**

| cohort | unrestricted | parity-restricted |
|---|---|---|
| INUENDO (PFNA, fecundability) | FR 0.80 [0.69–0.94] | **not replicated** — authors' own words |
| INUENDO (PFNA, infertility) | OR 1.53 [1.08–2.15] | **not replicated** |
| MoBa (PFOSA, fecundability) | FOR 0.85 [0.83–1.09] | FOR 0.91 [0.71–1.17], null |

Call 2 pre-committed to the two-track split on the mechanism — PFAS leave the body through pregnancy,
lactation and menstruation, so parity causes exposure — and predicted the restricted track would be
weaker. It is, in two independent cohorts, and the finding comes from inside the literature rather
than being imposed on it. **The chapter's PFAS verdict should rest on the restricted track and must
not report the unrestricted estimates as the result.**

Three further findings:

1. **Adjusting for parity is not restricting on it, and the distinction decides the verdict.**
   S-PRESTO — preconception-measured, the best exposure timing held — finds PFDA FR 0.90 [0.82, 0.98],
   PFOS 0.88 [0.79, 0.99], mixture 0.89 [0.73, 1.02], and *adjusts* for parity as a covariate. Parity
   is on the path from prior reproduction to exposure, so adjustment leaves the channel partly open
   and can induce collider bias. **`PARITY_HANDLING` needs four levels, not Call 2's implied two:**
   `nulliparous_restricted` / `parity_stratified` / `parity_adjusted` / `none`. Only the first two
   enter the restricted track. A refinement to the frozen scope, recorded as one.
2. **The microplastics PRIMARY cell holds five reviews and no effect estimate.** Its five empirical
   records all estimate fertility *inputs* — sperm parameters, retrieved oocytes, AMH — are small and
   largely ART-derived, and their p-values cluster at the margin (0.041, 0.056, 0.080, 0.083, 0.091).
   The one strong result (p = 0.0003) attaches to IVF fertilization rate, which Wall 4 routes to A.17.
   A verdict of **Very Low / no rateable evidence** is defensible, and it is a finding rather than a
   search gap: the completeness bypass guaranteed every both-axes plastic record was read.
3. **Five rows are `NUMERIC_UNRECOVERED`.** Decimals split across the PDF/XML-to-text boundary, so
   direction and p-value survive but point estimates do not. Recorded as missing rather than
   reconstructed — a number transcribed wrongly is worse than one recorded absent, and all five are
   on the microplastics side where an invented figure would do most damage.

**Not poolable yet.** PROTOCOL §5.9 wants three estimates sharing family, estimand level, sex stratum
and parity handling; the restricted track has two rows across two cohorts, one with no point estimate.
The honest output is narrative synthesis centred on the two-track disagreement.

**2026-08-14 — stage 12: both chapters drafted.** `output/chapters/microplastics-pfas-reproductive-pfas.md`
(2,515 words) and `…-microplastics.md` (2,043 words), each carrying all eleven §6 sections and each
naming the other as a required companion read. Written against the project's stop-slop rules:
no em dashes, active voice, jargon replaced with what it denotes.

Every study cited by author name was re-verified against a live record first, given that Call 4 found
three of four v5 seminal citations wrong. That check changed several attributions I would otherwise
have got wrong from the anchor set: the INUENDO cohort paper is **Jørgensen** et al. 2014, the MoBa
brief report is **Whitworth** et al. 2016, the Singapore preconception cohort is **Cohen** et al.
2023, and the LIFE cycle-length paper is **Lum** et al. 2016. The follicular-fluid ovarian-reserve
study (**Ferraz** et al. 2026) is a Research Square **preprint** and the chapter says so in the
included-studies table.

The two chapters reach negative verdicts of different kinds and say so explicitly, since a reader who
takes them as equivalent will draw the wrong inference about what future evidence could change:
PFAS fails on evidence that exists and points the wrong way, and could only be reopened through the
replacement-compound arm; microplastics fails on evidence that does not exist, and one adequately
designed cohort could overturn it.

Also filed earlier as a **duplicate-record gate** (the Minderoo-Monaco Commission carries two DOIs with different
citation counts plus an erratum, so DOI-level dedup double-counts it), and a correction to B.7's
scope, which wrongly lists B.6 among the hypotheses whose exposure post-dates its phenomenon — B.6's
exposure is older than the SDT; only its *measurement* is recent.
