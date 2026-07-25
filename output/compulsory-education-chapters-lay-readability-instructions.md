# Compulsory-Education Chapter Lay-Readability Review

Read both chapter drafts section by section, using the CSV as the checklist.

- Enter `PASS` in `ra_readability_decision` if a smart undergraduate can follow the section and
  its confidence matches the cited evidence.
- Enter `FLAG` if anything is confusing, jargon-heavy, overconfident, contradictory, citation-
  mismatched, or numerically unsupported.
- For a flag, enter one of `CLARITY`, `JARGON`, `OVERCONFIDENCE`, `CONTRADICTION`,
  `CITATION`, or `NUMBER` in `ra_issue_type`, and explain the problem in `ra_note`.
- Enter `YES` in `needs_pi_decision` only when the issue changes the hypothesis definition,
  evidence routing, GRADE judgment, demographic-significance rule, or another protocol choice.

Do not edit `ai_precheck`. Every row must receive `PASS` or `FLAG`; blank means not yet reviewed.
