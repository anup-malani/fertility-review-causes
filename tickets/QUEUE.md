# Work Queue

Last updated: 2026-08-25

Pick the first open ticket assigned to you or `any`. Before starting, pull/sync, then **claim** it
before doing the work. The active mode is **Mode B (branch-per-ticket)** — the simplest path is
`scripts/ticket.sh claim NNN`, which creates and pushes the `NNN-slug` branch and flips the
ticket status; then move its row to **In progress** below. (See `README.md` for the full loop and
the Mode A fallback.) Do not start a blocked ticket until its dependency is done. Parallel-safe
tickets can be worked concurrently.

> **The B.1 ticket chain was renumbered on 2026-07-25 (032–037 → 041–046).** TICK-032 had been
> assigned twice while the B.1 and schooling workstreams sat unmerged: to B.1 full-text retrieval and
> to the compulsory-education split. Alexandra's TICK-032 keeps the number; the whole B.1 chain moved
> up so it stays contiguous and no number is ambiguous.
>
> | Was | Now | Ticket |
> |---|---|---|
> | TICK-032 | [TICK-041](TICK-041-b1-fulltext-screen-retrieval.md) | B.1 full-text screen and retrieval |
> | TICK-033 | [TICK-042](TICK-042-b1-effect-extraction.md) | B.1 effect extraction |
> | TICK-034 | [TICK-043](TICK-043-b1-risk-of-bias.md) | B.1 risk of bias |
> | TICK-035 | [TICK-044](TICK-044-b1-status-fertility-meta-analysis.md) | B.1 meta-analysis |
> | TICK-036 | [TICK-045](TICK-045-b1-demographic-significance.md) | B.1 demographic significance |
> | TICK-037 | [TICK-046](TICK-046-b1-chapter-finalization.md) | B.1 chapter finalization |
>
> **Commits pushed before 2026-07-25 name the old numbers.** Read `TICK-032` through `TICK-037` in any
> commit message dated 07-21 to 07-25 against this table; in commit messages from Alexandra's schooling
> workstream, `TICK-032` means the compulsory-education split and needs no translation.
>
> **Next free number is TICK-073.** Claim a number by pushing its QUEUE.md row before starting work,
> not after. That is what would have prevented the collision. TICK-047 through TICK-053 were claimed
> for the D.3.b climate-anxiety chain on 2026-07-27; TICK-054 (A.10) and TICK-055 (C.2.c) on
> 2026-07-31; TICK-056 opens C.2.c library retrieval.
>
> **One further renumber on 2026-08-02: TICK-061 → TICK-060.** The number 060 was first given to a
> D.1.a search-scope ticket that was withdrawn before anyone claimed it, and the ticket-creation-rule
> ticket moved down into the freed number so the sequence stays contiguous.
> **Commits `1cfaebe`, `bd7e3be`, `ae14c64`, `9449f01` and PR #2 all name TICK-061 and mean the
> ticket-creation-rule ticket, now TICK-060.** One commit, `eecf024`, names TICK-060 and means the
> withdrawn D.1.a ticket; its full text is recoverable with
> `git show eecf024:tickets/TICK-060-d1a-search-scope.md`.

---

## Open — can start now

| Ticket | Title | Assigned | Parallel-safe |
|--------|-------|----------|---------------|
| [TICK-071](TICK-071-dating-apps-union-formation-friction.md) | A.24 Dating Apps and Union-Formation Friction | Shravan | yes |
| [TICK-070](TICK-070-twinning-multiple-births.md) | A.12 Twinning Rates and Multiple Births | Shravan | yes |
| [TICK-069](TICK-069-despair-hopelessness-fertility.md) | D.3.c Despair and Hopelessness | Shravan | yes |
| [TICK-048](TICK-048-d3b-fulltext-retrieval.md) | D.3.b full-text retrieval — mirror the B.1 scripts; realized-8 and desire-independence-4 first. **Watch the OA rate: it is what decides whether D.3.b avoids B.1's selection problem** | any | yes (with the full-62 half of 047) |
| [TICK-039](TICK-039-compulsory-education-chapter-readability.md) | Compulsory-education chapter lay-readability review | Alexandra | no |
| [TICK-030](TICK-030-replicate-gacs-agricultural-mode-production.md) | Replicate GACS for agricultural mode of production | any | no |
| [TICK-041](TICK-041-b1-fulltext-screen-retrieval.md) | **B.1 library retrieval of the 71 missing PDFs — needs a human with Zotero + UChicago proxy.** Automated ceiling hit at 20/95; the B.1 pooled estimate rests on 5 studies until this moves | Shravan or Alexandra | no |
| [TICK-002](TICK-002-cultural-count-fix.md) | Fix Cultural-count in Merge Notes | any | yes |
| [TICK-003](TICK-003-promote-batch-edits-lesson.md) | Promote batch-edits lesson to decisions/ | any | yes |
| [TICK-004](TICK-004-gitignore-workflows.md) | Revisit .gitignore for .claude/workflows/ | any | yes |
| [TICK-001](TICK-001-hypotheses-review.md) | PI review of HYPOTHESES.md | Anup | yes |
| [TICK-005](TICK-005-protocol-readability-pass.md) | PI + RA readability pass on PROTOCOL.md + RA-PLAYBOOK.md | Anup + RAs | yes |

## In progress — claimed, do not duplicate

> Rows with `—` in the **Branch** column were claimed under Mode A, before the 2026-08-02 switch to
> Mode B. They are valid claims, but `scripts/ticket.sh claim` cannot see them: its only collision
> check is whether a `NNN-*` branch exists on `origin`. **Read this board before claiming** until
> these rows have drained.

> **2026-08-15 — TICK-062 through TICK-068 were added to this board retroactively.** `ticket.sh claim`
> leaves the board move to be done by hand, and it was never done on `main` for any of them: all seven
> had live branches on `origin` while this file still advertised them under *Open — can start now*.
> One attempt exists, commit `1399787`, which removed TICK-064 from Open and wrote the replacement row
> for TICK-062 — right timestamp, wrong ticket — on a branch that was never merged. Claim times below
> are recovered from each `claim TICK-NNN` commit. **Merging TICK-067 is the durable fix**; until then
> the board move stays manual and this failure will recur.

| Ticket | Title | Owner | Branch (the claim) | Claimed (UTC) | Touches |
|--------|-------|-------|--------------------|---------------|---------|
| [TICK-072](TICK-072-art-access-fertility-recovery.md) | A.17. Assisted Reproductive Technology Access — **boundary inherited from A.12's scope-freeze**: ART live births = ART deliveries x (1 + *m*); A.17 owns the deliveries, A.12 owns only the multiplier, additively separable. Goldset scripts start at **185** (max across every branch, not main's 88) | Shravan | `072-art-access-fertility-recovery` | 2026-08-25T15:50:40Z | `literature/search-logs/art-access-fertility-recovery-*`, `extraction/art-access-fertility-recovery-*`, `output/chapters/art-access-fertility-recovery.md`, `source/build/goldset/185*` |
| [TICK-068](TICK-068-microplastics-pfas-reproductive.md) | B.6. Microplastics and PFAS in Reproductive Tissues — both chapter drafts on the PROTOCOL §6 template; last commit 2026-08-14 | Shravan | `068-microplastics-pfas-reproductive` | 2026-08-14T14:23:49Z | `literature/search-logs/microplastics-pfas-reproductive-*`, `extraction/microplastics-pfas-reproductive-*`, `output/chapters/microplastics-pfas-reproductive.md`, `source/build/goldset/13*` |
| [TICK-067](TICK-067-automate-ticket-claim-loop.md) | Automate the QUEUE.md board move in `scripts/ticket.sh claim` — **built and verified on its branch, unmerged.** This is the fix for the defect that left every row below missing from this board | Shravan | `067-automate-ticket-claim-loop` | 2026-08-13T20:13:46Z | `scripts/ticket.sh`, `tickets/README.md`, `tickets/opening-a-chapter-ticket.md` |
| [TICK-066](TICK-066-antidepressants-ssri-subfecundity.md) | B.7. Antidepressants and Pharmacological Subfecundity — chapter and verdict drafted; carries a script-numbering flag; last commit 2026-08-12 | Shravan | `066-antidepressants-ssri-subfecundity` | 2026-08-12T19:28:10Z | `literature/search-logs/antidepressants-ssri-subfecundity-*`, `extraction/antidepressants-ssri-subfecundity-*`, `output/chapters/antidepressants-ssri-subfecundity.md` |
| [TICK-065](TICK-065-fetal-loss-intrauterine-mortality.md) | B.5. Fetal Loss and Intrauterine Mortality — chapter drafted through the verdict section; last commit 2026-08-11 | Shravan | `065-fetal-loss-intrauterine-mortality` | 2026-08-11T20:00:22Z | `literature/search-logs/fetal-loss-intrauterine-mortality-*`, `extraction/fetal-loss-intrauterine-mortality-*`, `output/chapters/fetal-loss-intrauterine-mortality.md` |
| [TICK-064](TICK-064-child-centeredness-intensive-parenting.md) | D.2.d Child-Centered Intensive Parenting Norms — **chapter drafted, NOT review-ready**; screen at 21% with 53 of 76 batches outstanding, and the 9 primary-cell candidates need a full-text routing pass | Shravan | `064-child-centeredness-intensive-parenting` | 2026-08-08T16:02:45Z | `literature/search-logs/child-centeredness-intensive-parenting-*`, `extraction/child-centeredness-intensive-parenting-*`, `output/chapters/child-centeredness-intensive-parenting.md` |
| [TICK-063](TICK-063-caldwell-wealth-flows-westernization.md) | D.1.b Cultural Westernization and Developmental Idealism — interim chapter on the 17 retrieved studies; last commit 2026-08-07 | Shravan | `063-caldwell-wealth-flows-westernization` | 2026-08-02T13:17:32Z | `literature/search-logs/caldwell-wealth-flows-westernization-*`, `extraction/caldwell-wealth-flows-westernization-*`, `output/chapters/caldwell-wealth-flows-westernization.md` |
| [TICK-062](TICK-062-postmaterialism-individualism-secularization.md) | D.1.a Postmaterialism, Individualism, and Secularization — snowball round 1 done, round 2 required; last commit 2026-08-03 | Shravan | `062-postmaterialism-individualism-secularization` | 2026-08-02T13:09:21Z | `literature/search-logs/postmaterialism-individualism-secularization-*`, `extraction/postmaterialism-individualism-secularization-*`, `output/chapters/postmaterialism-individualism-secularization.md` |
| [TICK-055](TICK-055-c2c-housing-search-scope.md) | C.2.c search scope — tenure-conditional sign (price is a cost to renters, a wealth gain to owners), pooling rule, and the C.3.e wall that a shared seminal citation proves is broken | Shravan | — | 2026-07-31T00:00:00Z | `literature/search-logs/housing-costs-search-scope.md` |
| [TICK-054](TICK-054-a10-search-scope.md) | A.10 search scope — **drafted, PARKED pending Anup** on the unenumerated war-shock hypothesis and the non-additive-proximate-causes rule. Anchor sourcing is not blocked by the park | Shravan | — | 2026-07-31T00:00:00Z | `literature/search-logs/sex-ratio-marriage-market-search-scope.md` |
| [TICK-049](TICK-049-d3b-effect-extraction.md) | D.3.b effect extraction — realized track first-pass done, **0 of 11 rows poolable; no recoverable CIs**; second-reader pass outstanding | Shravan | — | 2026-07-27T00:00:00Z | `extraction/climate-anxiety-eco-doomerism-{studies,effects-realized}.csv` |
| [TICK-047](TICK-047-d3b-ra-gate.md) | D.3.b RA gate — boundary calls + 122 `INSUFFICIENT_INFO`; decisive-12 half gates extraction, Wall 1 (D.1.a) misroutes sampled first | Shravan | — | 2026-07-27T00:00:00Z | `extraction/climate-anxiety-eco-doomerism-ra-gate.csv`; `literature/search-logs/climate-anxiety-eco-doomerism-ra-gate-log.md` |
| [TICK-046](TICK-046-b1-chapter-finalization.md) | B.1 chapter finalization — **RA work complete, awaiting Anup's review**; PI packet has 6 numbered decisions | Shravan | — | 2026-07-25T00:00:00Z | `output/chapters/evolutionary-sex-drive-contraceptive-decoupling{,-pi-review-packet}.md` |
| [TICK-019](TICK-019-oas-demographic-significance-and-chapter.md) | OAS demographic significance and hybrid chapter draft | Alexandra | — | 2026-07-17T14:45:00Z | `output/chapters/old-age-security-pension-crowdout.md`; OAS evidence records |
| [TICK-031](TICK-031-replicate-gacs-child-labor-schooling.md) | Replicate GACS for child-labor laws and compulsory schooling | Alexandra | — | 2026-07-16T22:00:00Z | `source/build/goldset/`; `literature/search-logs/child-labor-laws-and-schooling-*`; related outputs/status files |

## Blocked — waiting on dependency

| Ticket | Title | Assigned | Blocked by |
|--------|-------|----------|------------|
| [TICK-050](TICK-050-d3b-risk-of-bias.md) | D.3.b risk of bias (adds a common-method-bias domain) | any | TICK-049 |
| [TICK-051](TICK-051-d3b-two-track-synthesis.md) | D.3.b two-track synthesis; adjusted-vs-unadjusted is the central test | any | TICK-049 |
| [TICK-052](TICK-052-d3b-demographic-significance.md) | D.3.b demographic significance (SDT only) | any | TICK-050, TICK-051 |
| [TICK-053](TICK-053-d3b-chapter-finalization.md) | D.3.b chapter finalization and PI review | any | TICK-052 |
| [TICK-006](TICK-006-osf-preregistration.md) | OSF pre-registration | Anup | TICK-001, TICK-005 |
| [TICK-009](TICK-009-literature-search-mjs.md) | Implement literature-search.mjs | any | TICK-001 |
| [TICK-012](TICK-012-prepilot-time-cost.md) | Pre-pilot (Anup + Claude): time-cost/income-substitution | Anup + Claude | TICK-001, TICK-009 |
| [TICK-010](TICK-010-pilot-run.md) | RA pilot Phase 1: old-age security/pensions | All three | TICK-012 |

## Done

| Ticket | Title | Closed |
|--------|-------|--------|
| [TICK-061](TICK-061-one-ticket-per-hypothesis.md) | One ticket and one branch per hypothesis; PROTOCOL §5 stages become the checklist. **Pending PI confirmation at the Monday sync** | 2026-08-02 |
| [TICK-060](TICK-060-document-ticket-creation-rule.md) | Document where ticket creation happens under Mode B, plus the four `ticket.sh` constraints on new ticket files. First ticket run end-to-end through the Mode B loop. **Numbered TICK-061 in commit history** | 2026-08-02 |
| [TICK-008](TICK-008-collab-system-design.md) | Design team collaboration/ticketing system; Mode B implementation and `scripts/ticket.sh` | 2026-08-02 |
| [TICK-059](TICK-059-rewrite-marriage-market-voice-stack.md) | Rewrite marriage-market chapter with voice-stack | 2026-08-01 |
| [TICK-058](TICK-058-marriage-market-assortative-mating-scoping.md) | Marriage-market and assortative-mating scoping search and chapter scaffold | 2026-08-01 |
| [TICK-057](TICK-057-install-voice-stack.md) | Install voice-stack for Codex | 2026-08-01 |
| [TICK-056](TICK-056-c2c-library-retrieval.md) | C.2.c library retrieval — identified core 15/15 via Zotero; associational remainder closed with a recommendation not to pursue | 2026-07-31 |
| [TICK-045](TICK-045-b1-demographic-significance.md) | B.1 demographic-significance pass | 2026-07-25 |
| [TICK-044](TICK-044-b1-status-fertility-meta-analysis.md) | B.1 status-fertility meta-analysis (5 studies; see ticket for the three cautions) | 2026-07-25 |
| [TICK-043](TICK-043-b1-risk-of-bias.md) | B.1 risk-of-bias assessment (4 of 5 studies serious) | 2026-07-25 |
| [TICK-042](TICK-042-b1-effect-extraction.md) | B.1 status-fertility effect extraction (17 effects / 5 studies, bounded by TICK-041) | 2026-07-25 |
| [TICK-040](TICK-040-finish-maternal-education-tempo-draft.md) | Finish maternal-own-education compulsory-schooling tempo draft | 2026-07-25 |
| [TICK-038](TICK-038-nest-schooling-teen-births-under-tempo.md) | Nest compulsory-schooling teenage births under tempo postponement | 2026-07-24 |
| [TICK-032](TICK-032-split-compulsory-education-hypotheses.md) | Split compulsory education into value-of-children and teenage-birth hypotheses | 2026-07-24 |
| [TICK-020](TICK-020-oas-theory-stream.md) | OAS theory stream for JEL-style mechanism section | 2026-07-11 |
| [TICK-007](TICK-007-gift-shravan-claude-max.md) | Gift Shravan Claude Max | 2026-06-14 |
| [TICK-011](TICK-011-hypotheses-recategorization.md) | Recategorize HYPOTHESES.md | 2026-06-14 (merged into TICK-001) |
| [TICK-013](TICK-013-agent-interop-doc.md) | Document Claude / Codex interop | 2026-06-27 |
| [TICK-014](TICK-014-meta-analysis-paper-pipeline-design.md) | Design meta-analysis-to-paper pipeline | 2026-07-03 |
| [TICK-015](TICK-015-oas-fulltext-screen.md) | OAS full-text screen and retrieval reconciliation | 2026-07-03 |
| [TICK-016](TICK-016-oas-data-extraction.md) | OAS full-text data extraction | 2026-07-09 |
| [TICK-017](TICK-017-oas-risk-of-bias.md) | OAS risk-of-bias assessment | 2026-07-09 |
| [TICK-018](TICK-018-oas-effect-harmonization-meta-analysis.md) | OAS effect harmonization and meta-analysis | 2026-07-09 |
| [TICK-021](TICK-021-oas-target-period-derivation.md) | Derive OAS target-period relevance from verified study windows | 2026-07-09 |
| [TICK-022](TICK-022-oas-multi-outcome-effect-extraction.md) | OAS multi-outcome effect extraction | 2026-07-10 |
| [TICK-023](TICK-023-oas-review-sheet-source-columns.md) | OAS effect review sheet source columns | 2026-07-10 |
| [TICK-024](TICK-024-oas-adjudicate-effect-review.md) | OAS adjudicate effect extraction review | 2026-07-10 |
| [TICK-025](TICK-025-oas-meta-analysis-readiness.md) | OAS meta-analysis readiness analysis | 2026-07-11 |
| [TICK-026](TICK-026-oas-sign-orientation-treatment-scale.md) | OAS sign orientation and treatment-scale coding | 2026-07-11 |
| [TICK-027](TICK-027-oas-pooling-rule.md) | OAS conservative pooling rule | 2026-07-11 |
| [TICK-028](TICK-028-oas-tfr-transition-classification.md) | OAS TFR-based transition classification | 2026-07-11 |
| [TICK-029](TICK-029-oas-demographic-significance-table.md) | OAS demographic-significance table | 2026-07-11 |
