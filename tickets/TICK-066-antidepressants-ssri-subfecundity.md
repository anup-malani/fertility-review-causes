# TICK-066: B.7. Antidepressants and Pharmacological Subfecundity
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `antidepressants-ssri-subfecundity` — HYPOTHESES-v5.md §B.7
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/antidepressants-ssri-subfecundity-*, extraction/antidepressants-ssri-subfecundity-*, output/chapters/antidepressants-ssri-subfecundity.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [x] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [~] 5. Full-text retrieval
- [~] 6. Full-text screen, RA spot-checks 5–10%
- [~] 7. Extraction to `extraction/antidepressants-ssri-subfecundity.csv`, RA verifies a random 10%
- [~] 8. Risk-of-bias assessment per study
- [x] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [x] 10. Demographic significance against PM / FDT / SDT
- [~] 11. GRADE rating, 3 independent raters
- [x] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log
Legend: `[x]` done · `[~]` done as far as an automated pass can take it, human gate outstanding.

### 2026-08-12 — end-to-end run, Shravan

Branch `066-antidepressants-ssri-subfecundity`. Scripts **123–131** plus
`source/analysis/b7_demographic_significance.py` (20 tests passing).

**Verdict.** SDT only, post-1988 only. Causal credibility **Very low**; demographic significance
**not significant** at 0.08% of the post-1988 OECD TFR decline, 3.4% at the no-recuperation upper
bound, and 17.1% only at the corner that grants the highest prevalence, the strong end of a
confidence interval containing the null, and the assumption that a delayed conception is a lost
birth.

**The finding is an absence, and it is specific.** Of 420 records screened from a 6,798-record
frame, 71 speak to link 1 (medication → sexual function), 12 to link 3 (borrowed from A.14), and
**one** to link 2 (sexual function → coital frequency) — a qualitative interview study of nine
women in a university repository. Exactly one study anywhere in the frame estimates a fertility
outcome against antidepressant exposure while adjusting for the indication (Yland et al. 2022,
FR 0.85 [0.65, 1.12]), and that paper says in its own introduction that nobody had done it before.

**67.6% of the SDT decline was complete before fluoxetine reached market in 1988.** This is Call 1
and it generalises to B.6, C.2.h, D.3.b and C.3.b; the ruling belongs in PROTOCOL §4.2, not here.

**A fourth anchor gate was added: the shadow-record gate.** `Editorial Comment to X`,
`Faculty Opinions recommendation of X`, `Re: X` and `Expression of Concern: X` defeat the existence,
version-of-record and book-canon gates by construction and resolve at overlap 1.0. Five fired on
this canon. On Montejo et al. 2001 neither index copy of the study carries a DOI while the Faculty
Opinions comment does, so a DOI-preferring resolver anchors a 1,022-patient study to a one-paragraph
note. The Expression of Concern on Safarinejad 2008 is carried as an integrity flag rather than
discarded.

**Three defects found by auditing refusals rather than admissions**, all recorded in the anchor log:
the shadow gate's general containment rule refused five distinct works on a three-token anchor;
Alwan et al. 2007 resolved to a digest reprint rather than the NEJM original, which is the exact
failure that candidate was planted to test; and the fix for that created its own regression, sending
Serretti and Chiesa 2009 to a conference abstract because the tie-break's last term was DOI string
order.

**SCRIPT-NUMBER COLLISION ACROSS UNMERGED BRANCHES — needs a decision.** 88 is the highest on
`main`, but D.1.a holds 95–115, D.1.b 95–102, D.2.d 103–108 and B.5 115–122, so **103–115 is claimed
three times over**. This run starts at 123, above every number in use anywhere, but the collision is
real and will surface at merge. It is the same hazard the 2026-07-25 B.1 renumber addressed; the
fix then was a renumber table in QUEUE.md, and something similar will be needed again.

### Open, in priority order

1. **RA gate signature** — `extraction/antidepressants-ssri-subfecundity-ra-gate.csv`, 25 rows.
2. **Library retrieval of 14 primary-cell records.** Two matter most and both have PMC identifiers
   that are not in the open-access subset: the AJOG female-side companion to Yland et al.
   (PMC11064128) and the *Fertility and Sterility* study naming depression and antidepressant use
   together against male and female fertility (PMC5973807). Automated routes are exhausted — the
   route ladder already doubled the yield from 3 to 6 of 20 — and the rest is a proxy task.
   The paywalled US age-and-sex prevalence series matters more to the verdict than any single
   effect size and should be retrieved with them.
3. **Independent GRADE re-rating.** Rated by one analyst across three lenses; a panel of three is
   required by §5.11 and the composite rating sits on the Low/Very-low boundary.
4. **PI answers on Calls 1–5** (see the chapter's §10).
5. **TICK-001 corrections to HYPOTHESES-v5 §B.7:** the seminal list's "Beeder and Bhatt PMC scoping
   review (2025)" is Beeder and Samplaski, *International Journal of Urology*, 2019; and the claim
   text locates the mechanism in women while the measured fertility evidence is male.
