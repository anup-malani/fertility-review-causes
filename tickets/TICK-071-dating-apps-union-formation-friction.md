# TICK-071: A.24 Dating Apps and Union-Formation Friction
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `dating-apps-union-formation-friction` — HYPOTHESES-v5.md §A.24
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/dating-apps-union-formation-friction-*, extraction/dating-apps-union-formation-friction-*, output/chapters/dating-apps-union-formation-friction.md

## Acceptance criteria
- [x] 2. Search strategy and scope **DRAFTED, not frozen** — `literature/search-logs/dating-apps-union-formation-friction-search-scope.md` (2026-08-24). 9 walls, 9 estimand cells, 5 PI calls open.
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/dating-apps-union-formation-friction.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-24 — reconnaissance and scope draft

Pre-scope recon (`source/build/goldset/170_a24_recon_probe.py`, 65 requests, 0 failed) plus a
named-work re-check (`171_a24_named_recheck.py`, 17 requests, 0 failed). Reports at
`literature/search-logs/dating-apps-union-formation-friction-{recon-probe,named-recheck}.md`;
scope at `-search-scope.md`.

Four findings that set the shape of the chapter:

- **The primary cell is empty and it was measured, not assumed.** Dating-app exposure against a
  population fertility quantity returns **11 records**, and no record among them estimates the
  effect; the citation-ranked head is a marriage-market paper, a popular history of romance, and two
  survey data-resource profiles. A.24 is a three-link chain (apps -> partnering -> unions -> births)
  and only the middle link has been estimated. Same shape as B.7.
- **Where field evidence exists it runs AGAINST the hypothesis.** Rosenfeld 2017 (*Sociological
  Science*) tests the choice-overload critique directly and finds meeting online does not predict
  breakup and predicts *faster* transitions to marriage; Billari Giuntella & Stella 2019
  (*Population Studies*) and Kalabikhina et al. 2020 both find *positive* broadband effects on
  fertility. The theory does not give the sign and the screen may not presume it.
- **The mechanism and the outcome live in disjoint literatures.** Choice overload is genuinely
  measured — Pronk & Denissen's rejection mind-set (27% fall in acceptance), D'Angelo & Toma,
  and one randomized field experiment with matching outcomes (Jung et al. 2021, *ISR*) — but the
  friction literature reaches a demographic outcome in 34 records, whose head is economic
  search-friction theory, a different sense of the word. This is what a Low GRADE for indirectness
  will rest on.
- **The identified variation for this chapter is C.2.h's variation.** App-specific quasi-experiments:
  33 records, none a design. Every reachable estimate runs on broadband/3G/cellular rollout and none
  says "dating app" in its abstract, so Wall 9 is **declared unenforceable** and bypassed on seed
  provenance with no dating-vocabulary requirement — A.12's Wall 8 lesson applied before the fact
  rather than after.

**Workflow finding, inherited defect.** 170_'s pass-2 named-work retries returned **zero for all
fifteen** queries. `filter=title.search:` matches the title field only, so any retry carrying an
author surname is unsatisfiable by construction, and 171_ shows `search=` does not match author names
either. Every chapter's recon script carries this pass-2 pattern, inherited from B.5, so every one of
them has been generating fake zeros. The fix (retry via `raw_author_name.search:` or by DOI) belongs
in the shared scaffold; flagged, not edited from this branch.

Two citation-hygiene items carried to A3: OpenAlex indexes Rosenfeld 2017's author as **"Michael
Rosenfield"**, which an author gate will refuse on one of the chapter's most important include-side
anchors; and both `Love Unshackled` and Ortega & Hergovich resolve to preprint/version-of-record
splits. Finkel et al.'s review resolved on neither endpoint and is recorded as **unresolved by query,
not absent**.

Scripts numbered 170-171 against the cross-branch high-water mark of 169; `main` alone would have
said 89 and collided with six live branches.

Next: A3 cold-start anchor resolution (script 172), 25 anchors, one routing decoy per enforceable
wall.
