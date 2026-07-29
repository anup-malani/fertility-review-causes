# Handoff — PI voice rewrites, fertility-explanations review

**Session:** 2026-07-26 → 07-29 · **Branch:** `pi-voice-rewrites` (pushed to origin)
**Next session should read this file first, then `PROTOCOL.md` §6 and §6.1, then `.claude/skills/rewrite-chapter/SKILL.md`.**

---

## Current state

Four chapters are finished and clean. A fifth is screened but not drafted.

| Hypothesis | Current file | Words | Status |
|---|---|---|---|
| A.10 | `output/chapters/tempo-effects-birth-postponement-compulsory-schooling-pi-v5-memo.md` | 4,947 | Final. Retitled *Compulsory Schooling and the Fertility of the Female Student*. Two findings, six verdict rows. |
| B.4 | `output/chapters/compulsory-education-child-economic-value-pi-v6-memo.md` | 4,479 | Final. GRADE referral discharged. |
| B.15 | `output/chapters/old-age-security-pension-crowdout-pi-v4-memo.md` | 5,898 | Final. |
| B.1 | `output/chapters/evolutionary-sex-drive-contraceptive-decoupling-pi-v5-memo.md` | 5,689 | Final except one PI decision, below. |
| D.3.b | `output/chapters/climate-anxiety-eco-doomerism.md` | — | **Not drafted.** RA's structural skeleton; no full text retrieved, no effects extracted, everything PENDING. |

Every version is on disk as `-pi-v<N>-memo.md`. PI-annotated stages carry `-AM` and are the specification for the version after them. Do not overwrite an `-AM` file.

All four finished chapters pass: zero clefts, zero em-dashes, zero teammate names in reader-facing prose, zero positional back-references, every estimate exact against its chapter's `numbers-v1.md`.

---

## Pending tasks, most immediate first

**1. B.1's bottom line — waiting on the PI, blocks nothing else.**
The bottom-line box says the status-and-reproduction claim "is well supported." Four paragraphs later the same box says "the positive baseline the theory needs is not established by this review's evidence." Both cannot stand. The claim is comparative and needs a positive baseline; the re-pooled contraception-absent cell is −0.0585 with an interval crossing zero. Do not resolve this without him.

**2. Referent audit on B.4 and B.15.** The rule now exists (PROTOCOL §6.1) but these two predate it. B.4 has 12 bare "the hypothesis"; B.15 has 2. Neither has been checked by reading, only by grep. B.1's fix is the worked example of what this looks like: coin a tag, use it everywhere, open Section 1 formulaically.

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
