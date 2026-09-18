# TICK-090: Scope-number checks assert against a copy of the table, not the table — `406` checks none of A.6's numbers
**Status:** open
**Assigned:** any
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** source/build/goldset/406_a6_scope_number_check.py, literature/search-logs/stigma-reduction-contraception-abortion-search-scope.md, docs/, tickets/QUEUE.md

## Description
Every stage-2 scope doc ends with a provenance line claiming that no number in it is retyped from
memory (`generate-result-tables-never-retype`). `406` exists to make that claim checkable for A.6.
It does not.

Counted on branch `087-stigma-reduction-contraception-abortion`:

| `406` contains | n |
|---|---|
| `want(label, expected)` — compares the measurement JSON against a value hardcoded in `406` | 25 |
| `in_doc(string)` — checks the scope doc carries a required string | 4 |
| …of those 4, how many carry a digit | **0** |
| `fails.append` on computed arithmetic (shares, multipliers, gains) | 21 |

So `406` verifies that the numbers typed into `406` match the JSON. **It never reads a number out of
A.6's scope document.** Editing any count, share or marginal gain in
`stigma-reduction-contraception-abortion-search-scope.md` leaves `406` passing. The hardcoded dict is
a second transcription of the table, so the check compares two copies and the artifact it is supposed
to police is not an input.

The same defect was written into `429` (TICK-089) and caught only because the checker was tested by
perturbation before being trusted: a missing string was detected, a changed number was not. `429` now
parses cells out of the markdown; see its docstring and the TICK-089 log for the shape of the fix.
A.6's scope doc is not a draft — TICK-087's chapter, GRADE rating and demographic-significance
verdict are all built on it — so this is a live exposure on a finished chapter, not a hygiene item.

## Acceptance criteria
- [ ] `406` reads A.6's scope-doc numbers out of the markdown and compares those against the JSON, in place of the hardcoded values.
- [ ] `406` is tested by perturbation: change a count, a share and a marginal gain in the scope doc, and record that each one makes it fail. A check that has not been made to fail is not a check (`validate-a-null-detector-on-positives`).
- [ ] The perturbation test is run for every class of number the doc carries, not one example — `429`'s first version caught missing strings and missed changed numbers, so classes fail independently.
- [ ] Any number in A.6's scope doc that turns out NOT to match `404`/`405` is corrected, and the correction is assessed for whether it reaches the chapter's verdict.
- [ ] The rule is written where the next author will read it before writing the next checker — a line in `docs/` or `AGENTS.md`: **assert against the artifact, never against a copy of it, and perturb before trusting.**
- [ ] Decide whether the check belongs per-chapter at all, or whether one shared checker driven by a per-chapter manifest replaces `406`/`429` and everything after them.

## Log
