# TICK-062: D.1.a Postmaterialism, Individualism, and Secularization
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `postmaterialism-individualism-secularization` — HYPOTHESES-v5.md §D.1.a
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/postmaterialism-individualism-secularization-*, extraction/postmaterialism-individualism-secularization-*, output/chapters/postmaterialism-individualism-secularization.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/postmaterialism-individualism-secularization-search-scope.md` (DRAFT, not frozen; Rulings 2 and 3 need PI sign-off)
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/postmaterialism-individualism-secularization.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log
- 2026-08-03 (Shravan/Claude): **scope drafted, deliberately NOT frozen.**
  `literature/search-logs/postmaterialism-individualism-secularization-search-scope.md`. Five strata,
  eleven walls, 25 estimand cells, ten required per-effect tags, five pre-registered rulings. The
  scoping brief was taken from the withdrawn D.1.a ticket, recoverable at
  `git show eecf024:tickets/TICK-060-d1a-search-scope.md`. Five things the drafting settled or
  surfaced beyond that brief:
  **(1) Two rulings cap the chapter's rating before any study is read, and neither is an RA call to
  make alone.** Ruling 2 bars value measures whose item content refers to children or family size
  from the causal pool, because regressing a person's childlessness on their own approval of
  childlessness estimates preference-outcome consistency rather than a causal effect. That removes
  most of `childlessness-as-acceptable-choice`, one of the five sub-claims the master list assigned
  here. Ruling 3 fixes an admissible-design ladder with pre-committed GRADE ceilings and puts
  country-level value-index-versus-TFR co-movement — **the canonical SDT evidence base** — at Tier 4
  with no causal weight, on three joint defects: about fifty units against a dozen collinear
  covariates, GDP among them, and countries not being independent draws because values diffuse across
  borders. Both are flagged for PI sign-off as a freeze condition.
  **(2) The strata are unequal enough that even search budget should not be split evenly.**
  Secularization is the only one of the five with a large individual-level literature and access to
  genuine natural experiments (state atheism campaigns, church-tax and blue-law reform, clergy-scandal
  shocks, compulsory secular schooling). Postmaterialism and individualism have a large theoretical
  and measurement literature and very few fertility estimates above Tier 4. Same shape as C.2.c's
  rent-identified stratum carrying that chapter.
  **(3) Wall 8 is a demonstrated failure, not a hypothetical one — the Lovenheim and Mumford problem
  again.** A.19's seminal list contains Fernández and Fogli 2009 and its `notes` field claims the
  epidemiological approach outright, but that design is the best available tool for D.1.a's claim
  because it holds prices and institutions fixed while culture varies. Resolved on proxy content:
  ancestral *fertility rate* tests persistence and routes to A.19; an ancestral *value measure* tests
  the content claim and routes here. Master-list note recommended for TICK-001, flagged not made.
  **(4) Non-additivity, third instance and materially worse than the first two.** A.10 → A.7 and
  C.2.c → A.23 are each one hypothesis with one mediator. D.1.a is a root cause whose whole pathway
  runs through four or five separately credited chapters (A.3, A.6, A.2/B.1, D.2.b, A.7) — three of
  which name D.1.a as their root cause in their own `notes`. If each proximate chapter claims its
  share and D.1.a claims the reduced form, the shares sum past 100% and the per-hypothesis verdict
  format breaks where a reader adds it up. Folded into the TICK-054 escalation, with the note that it
  is now a defect in the deliverable's format rather than an accounting nuisance.
  **(5) Two concrete search hazards worth catching before the query build.** The word *materialism*
  means opposite things in the two feeding literatures — Inglehart's materialist prioritizes security,
  the consumer-psychology materialist is acquisitive — so an undisambiguated term retrieves both and
  scores them in opposite directions. And much of this literature runs on a handful of survey
  instruments (WVS/EVS, ESS, GSS, DHS), so twenty papers on overlapping waves and countries are not
  twenty independent estimates; `DATA_SOURCE` is a required tag and a clustering variable in any
  pooled analysis.
  Also ruled: FDT-era evidence admitted (Princeton EFP secularization is measurement of the S3
  construct applied to the first transition), with the `phenomena` field escalated to TICK-001 as the
  third instance of the same restriction; and a sign convention orienting every effect toward the
  secular/postmaterialist pole, since S3 is almost always coded the other way and mixing flipped and
  unflipped estimates is a mechanical route to a null.
- 2026-08-03 (Shravan/Claude): opened and claimed. No prior D.1.a artifacts exist in
  `literature/search-logs/`, `extraction/`, or `output/chapters/`; the only inbound material is the
  17 records the D.3.b RA gate routed to `OFF_POSTMATERIALIST_D1a`.