> **SUPERSEDED 2026-07-31.** Read `handoffs/2026-07-31-resume-here.md` instead.
> This file is kept as the record of the voice-rewrite session. Its task list is
> done or overtaken, and its hypothesis codes (A.10, B.4, B.15) are stale — the
> master list has those at A.11, C.3.b and C.3.c.

# Handoff — PI voice rewrites, fertility-explanations review

**Session:** 2026-07-26 → 07-29 · **Branch:** `pi-voice-rewrites` (pushed to origin)
**Next session should read this file first, then `PROTOCOL.md` §6 and §6.1, then `.claude/skills/rewrite-chapter/SKILL.md`.**

---

## Current state

Four chapters are finished and clean. A fifth is screened but not drafted.

| Hypothesis | Current file | Words | Status |
|---|---|---|---|
| A.10 | `output/chapters/tempo-effects-birth-postponement-compulsory-schooling-pi-v5-memo.md` | 4,947 | Final. Retitled *Compulsory Schooling and the Fertility of the Female Student*. Two findings, six verdict rows. Tag: the *own-schooling hypothesis*. |
| B.4 | `output/chapters/compulsory-education-child-economic-value-pi-v6-memo.md` | 4,479 | Final. GRADE referral discharged. Tag: the *lost-child-earnings hypothesis*. |
| B.15 | `output/chapters/old-age-security-pension-crowdout-pi-v4-memo.md` | 5,898 | Final. Tag: the *old-age-security hypothesis*, above the *retirement-asset* and *grandparent-time* channels. |
| B.1 | `output/chapters/evolutionary-sex-drive-contraceptive-decoupling-pi-v5-memo.md` | 5,689 | Final. Tag: the *delink-sex-and-reproduction hypothesis*, splitting into the *pre-contraceptive gradient* and the *dissociation under contraception*. |
| D.3.b | `output/chapters/climate-anxiety-eco-doomerism.md` | — | **Not drafted.** RA's structural skeleton; no full text retrieved, no effects extracted, everything PENDING. |

Every version is on disk as `-pi-v<N>-memo.md`. PI-annotated stages carry `-AM` and are the specification for the version after them. Do not overwrite an `-AM` file.

All four finished chapters pass: zero clefts, zero em-dashes, zero teammate names in reader-facing prose, zero positional back-references, every estimate exact against its chapter's `numbers-v1.md`. As of 2026-07-30 all four also carry a coined hypothesis tag, open Section 1 formulaically, write in one voice ("this review"), name each other in English one way each, and carry causal-credibility ratings in the bottom-line box.

**One follow-up ticket falls out of the B.1 split:** `source/analysis/b1_demographic_significance.py` hardcodes four channels and has no `PM_decoupling` row, so its generated verdicts CSV cannot reproduce the chapter's five-row table. Its `PM_dissociation` row is also stale on the substance, describing the superseded single-study cell, because the script derives it from an effects file the re-pool was never written into. That write-in is already ticketed in B.1's notes to co-authors; the script change is downstream of it.

---

## Pending tasks, most immediate first

**1. ~~B.1's bottom line~~ — DONE 2026-07-30, commit `9fa3664`.** The PI chose to split the status-and-reproduction claim into two separately rated halves, the *pre-contraceptive gradient* and the *dissociation under contraception*, following the A.10 multi-finding precedent. The GRADE and verdict tables both go to five rows and agree for the first time; previously the verdict table left its pre-modern row unlabeled by claim while the GRADE table labeled the same row "decoupling claim," and the generated CSV keyed it `PM_dissociation`. Recorded as an eighth protocol departure, because the new row postdates the three-rater panel and `b1_demographic_significance.py` still builds a four-row CSV from an effects file the re-pool was never written into.

**2. ~~Referent audit on B.4 and B.15~~ — DONE 2026-07-30, commits `3c5d97b`, `fa71b9b`, `46d9b16`. Extended to A.10.** Reading found roughly double what grep did: 22 untagged hypothesis references in B.4 (not 12), 9 in B.15 (not 2), 3 in A.10. All four chapters now coin a tag and open Section 1 formulaically — the *lost-child-earnings*, *old-age-security*, and *own-schooling* hypotheses join B.1's *delink-sex-and-reproduction* hypothesis.

The defect grep could never have found: **B.4 referred to A.10 under three different names** ("the chapter on the fertility of the female student", "the birth-postponement chapter", "the tempo chapter"), and one reference was a broken substitution left from the A.10 retitle reading "The chapter on tempo the fertility of the female student." A.10 likewise called B.4 by two names, two of them wrapped across lines and invisible to a single-line grep. The two chapters now name each other one way each, ten times and seven times.

Also fixed: B.4's 17 first-person instances normalized to "this review" (the PI's call, matching B.1 and B.15); numbered diagram arrows named in both A.10 and B.4; positional back-references removed from all three; B.15's orphaned pre-modern sentence in §11 given its own topic sentence; B.15's bottom-line box given a ratings paragraph so all four boxes now carry one.

Note for review: **B.4's commit diff includes a whitespace reflow to 100 columns**, so it reads as 165/162 lines. Use `git diff --word-diff HEAD~2 HEAD~1` or compare word multisets. B.15 and A.10 were done without a global reflow and their diffs are small.

**3. D.3.b.** Four screen artifacts at `temp/rewrite/climate-anxiety-eco-doomerism/`: `evidence-base-v1.md`, `extraction-plan-v1.md`, `questions-v1.md` (8 questions, unanswered), `outline-v1.md`. It cannot be drafted until extraction happens. The highest-value single action in the whole project right now is retrieving **Bisi, Sturm and Van Bavel (2024)**, `10.4054/demres.2024.51.2` — see the finding below.

**4. RAs owe three replies:** the 10% demographic-significance threshold, where the PDFs should live (Dropbox vs Git LFS), and the filename convention. All three emailed 2026-07-29 from `amalani@uchicago.edu`.

**5. PROTOCOL §4.2 still defines demographic significance by the 10% threshold.** All four chapters report shares plainly instead. They disagree until the RAs weigh in. The edit is one paragraph when they do.

**6. Lessons ledger for the voice system** — the PI asked for this to be assembled once the edits settled. They have. A partial field report exists at `/Users/amalani/Downloads/voice-system-fixes-brief-2026-07-26.md`, and nine voice tickets are filed in `assistants/voice/tickets/inbox/`.

---

## Two substantive findings that outrank the writing work

**B.1's central quantitative pattern reversed.** The chapter reported the status-fertility association as +0.19 where contraception is absent against +0.07 where present, an attenuation the hypothesis predicts. The +0.19 rested on von Rueden and Jaeggi alone. Four further contraception-absent estimates were sitting unused in `extraction/evolutionary-sex-drive-contraceptive-decoupling-effects-workflow.json` (records `W2791607709`, `W3124469204`, `W2163381596`, `W2117546824`). Pooled under the project's own DerSimonian-Laird method they give **r = −0.0585, 95% CI −0.163 to +0.047**. All four sensitivity specifications return a negative point estimate. Method, inputs, weights and sensitivities: `output/tables/evolutionary-sex-drive-contraceptive-decoupling-contraception-absent-pool.md`.

Caveat stated as prominently as the finding: **Sorokowski et al. (2013)** report +0.42 for men and +0.27 for women among the Yali, the largest positive contraception-absent values anywhere in the corpus. They reach the project only through a review that quotes them without a sample size, so no variance and no weight. The negative pool is computed without the estimate pointing hardest against it.

**D.3.b may be refuted by a paper inside its own screen.** Bisi, Sturm and Van Bavel (2024, *Demographic Research*) randomize a pessimistic against an optimistic climate vignette and measure fertility **desire**. D.3.b's whole claim is that ecological dread suppresses childbearing *while the desire for children remains intact*. The screen record reads `desire_for_children_held_fixed: no` and its summary says the manipulation raises the probability of low fertility desire. If the full text bears that out, the hypothesis collapses into D.1.a. It is one of only two randomized designs in 1,170 screened records, and the skeleton mentions them once in a subordinate clause. **Nobody has read the paper.**

---

## Key decisions the PI made, and why

- **Register: memo**, chosen over academic-econ after two drafts from one outline. An Opus judge preferred academic; the PI overruled it because the judge's margin rested on two defects fixable in the memo.
- **Audience: a generalist with undergraduate economics training, very little time, several distractions, who will not re-read a sentence.** She knows standard errors and significance. Explaining those to her is a defect.
- **Empirical strategy is now a required chapter section** (PROTOCOL §6, new §3). It defines the treatment, defines the outcome, states the ideal experiment, then names the limitations the practical design carries. Limitations that follow from the identification strategy stay separate from those that hold regardless.
- **A chapter may carry more than one finding, each rated separately.** A.10 does: an effect on birth timing and a separate effect on completed fertility. Its verdict table has six rows. PROTOCOL §6 amended to allow it. Rationale, in the chapter as a note to the RA: one averaged rating would describe neither finding.
- **Report shares plainly, do not narrate them against the 10% bar.**
- **Completed fertility in B.15 gets no pooled number** — the claim-relevant pool is k=2, below PROTOCOL §5 stage 9's threshold. Reported narratively with an RA note in the chapter text requesting the Danzer and Zyska standard error that would make k=3.
- **A.10's title stands** as the draft adopted it, and B.4's six cross-references were updated to match.

---

## Relevant paths

**Skill and protocol** — read before drafting anything
- `.claude/skills/rewrite-chapter/SKILL.md` — the four-phase pipeline and every settled decision
- `PROTOCOL.md` §6 (chapter template, Empirical strategy as §3), §6.1 (writing conventions)

**Per-chapter working artifacts** — `temp/rewrite/<slug>/` holds `claims-v1.md`, `numbers-v1.md` (the fidelity contract), `outline-v*.md`, `questions-v*.md`. `temp/` is gitignored, so these exist only on this machine.

**Analyses produced this session**
- `output/tables/old-age-security-pension-crowdout-grade-panel.csv` — three-rater panel, 12 rows
- `output/tables/compulsory-education-grade-panel-rerate.csv` — B.4's re-rate, Low confirmed 3/3
- `output/tables/old-age-security-pension-crowdout-restricted-pools.md`
- `output/tables/evolutionary-sex-drive-contraceptive-decoupling-contraception-absent-pool.md`
- `output/tables/superseded/` — the mis-briefed panel round, kept deliberately

**Voice system**
- `~/.claude/skills/rewrite-chapter/` does not exist; the skill is project-local and force-added past `.gitignore`
- `assistants/voice/tickets/inbox/` — nine tickets from this session
- `assistants/voice/export/voice-stack/` — export package the voice assistant built for the RAs, not yet delivered

---

## Resume instructions

**To continue chapter work:** read this file, then `PROTOCOL.md` §6 and §6.1, then the skill. The skill's "Settled decisions" section is binding and should not be re-litigated — it is the compressed output of five rounds of PI markup.

**When drafting, do not paraphrase `/write-as` into a prompt bullet.** That failure produced three rejected drafts. Either invoke the skill, or paste the memo CORE exemplar paragraphs from `~/.claude/refs/exemplars/memo.md` verbatim into the agent's context as imitation targets. The three that matter for this review are the two-part partition ("One is… The other is…"), the definitional move ("By X, I mean…"), and mechanism-first-magnitude-last.

**Run the referent audit by reading, not by grep.** Greps catch bare "the hypothesis", "stream", and bare section codes. They miss most of the class. Every real defect this session was found by a human read or an ad-hoc measurement, never by the automated screen.

**Do not trust a fidelity requirement you inherited without checking it.** "The contraception-absent side rests on a single study" was carried across four drafts as an untouchable fact and was false.

**Blocked on infrastructure:** none of the 25 PDFs in the retrieval manifest is in this working tree. `literature/pdfs/` is gitignored and holds only the Zelu working paper. Any task requiring a PDF read cannot be done here until the RAs answer the storage question.
