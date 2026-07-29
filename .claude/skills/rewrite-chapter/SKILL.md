---
name: rewrite-chapter
description: Rewrite an RA-drafted review chapter in the PI's voice by screening substance first, surfacing the decisions only the PI can make, and drafting from an approved outline rather than from the source prose. Use when the PI says "rewrite chapter X", "run the chapter rewrite on X", "screen X for a rewrite", or "/rewrite-chapter <slug>". Do NOT use to copy-edit an existing draft (that is /voice-check) or to draft something with no source chapter.
---

# rewrite-chapter

## Why this exists

Four rounds of rewriting the first batch of chapters fixed the prose every time and left the substance untouched. A four-part mechanism taxonomy survived three rewrites because no prose pass questions a taxonomy, it only finds better words for it. A section reviewing six studies the chapter had already declared off-target survived every version because the source had it. Both defects died the moment the PI read a draft and asked a question.

The lesson is that **rewriting a document anchors on that document**. Structure, section order, emphasis, and inclusions all carry forward untouched, and the expensive corrections arrive after three thousand words exist.

This skill moves the PI's judgment from after the draft to before it. He answers questions and edits an outline; the drafting happens against decisions already made.

---

## Settled decisions — do not re-litigate these

B.4 was taken through this pipeline first, over six versions and five rounds of PI markup. The following came out of it and now hold for every chapter. The finished B.4 is the reference model: `output/chapters/compulsory-education-child-economic-value-pi-v6-memo.md`.

**Register: memo.** Two drafts were produced from one outline, in academic-econ and memo, and the PI chose memo: "much better written and clearer... more efficient and accessible." An Opus judge had preferred academic; the PI overruled it, correctly, because the judge's margin rested on two defects that were fixable in the memo.

**Audience: a generalist with undergraduate economics training, very little time, and several distractions, who will not re-read a sentence.** She knows standard errors, confidence intervals, statistical significance, and what a meta-analysis pools. **Explaining any of those to her is a defect.** She does not know this literature, this project's pipeline, or demography. State the implication of a statistic, not the statistic.

**Every chapter gets an Empirical strategy section, between Theoretical mechanism and Search strategy.** The PI: "You did an outstanding job with the Empirical Strategies section. This is a template for what we should do in every chapter." It does four things in order:

1. **The treatment, defined.** Name the actual instruments and distinguish them from each other where the literature runs them together.
2. **The outcome, defined**, and why that outcome and not a neighbouring one.
3. **The ideal experiment.** What you would do with no constraints, holding fixed everything the hypothesis is not about.
4. **The practical design, and the limitations that follow from it.** Name each limitation and then **use the name downstream, never the list position.**

On point 4, a correction earned the hard way in B.4. Distinguish limitations that **follow from the identification strategy** from limitations that **hold regardless of it**. B.4 announced "four limitations follow from that substitution" when only three did; the fourth concerned which outcome studies measured, not how they assigned treatment, and would survive a perfect experiment. That error passed three drafts and two PI reads. When you enumerate, check that every item belongs to the class the opener names.

The gap between the ideal and the practical experiment also generates the **external-validity** analysis (across eras, across locations) and the **causation** analysis. Later sections should refer back to a limitation already named rather than introducing it fresh.

**Name limitations; never refer to them by position.** "The second and third limitations in Section 3" asks a reader with no time to scroll back and count. B.4 uses named handles (adoption endogeneity, policy bundling, the child-quality channel, the wrong-generation problem) twelve times. This was the single largest readability difference between the two register drafts.

**The topic-sentence standard, which is the rule the PI has enforced most often.** In his words: "Never use a topic sentence that, by itself, does not summarize the paragraph without any context other than the topic sentences and prior topic sentences," and, tightened: each should stand alone **without relying on other topic sentences**. His reader "would prefer to be able to read just the topic sentences and understand the whole argument."

Test it by extracting every topic sentence, **shuffling them**, and confirming each still makes sense out of order; then read them in order and confirm they carry the argument. Length is not the target, self-sufficiency is: a long topic sentence that carries its paragraph beats a short one that gestures at it. Rejected openers, for shape: "The first link holds." / "Three things limit the 8%." / "Two studies would move the verdict." / "The fourth qualification is that…" / any "which is the first step of the chain in Section 1."

**Tells earned on this project, beyond `ai-tells.md`.** Announce-then-state (if deleting a sentence loses no fact, delete it). Anthropomorphic inanimates ("earned their place", "sits underneath", "carries the whole effect", "generations sit in"). Figurative labels standing in for claims ("theory that reverses the arrow"). Unnamed demonstratives — every "that X" names X. Never name a teammate in reader-facing prose. Never describe methodology the project has not run; collaborator-facing material goes in `[Note to co-authors: ...]` at the end, not inline.

**Report shares plainly; do not narrate them against the 10% threshold.** A proposal to drop the threshold as a verdict device is with the RAs.

**Make headline estimates interpretable.** B.4 reported −0.301 children and, separately, a mean of 3.112, and never related them. State that the effect is about a tenth of the mean.

**Open with a bottom-line box** under the title: what the hypothesis claims, what the evidence base actually is, and the verdicts. A reader with ten minutes should not have to reach Section 9 to learn the answer.

## The four phases

### Phase 1 — Screen (agent, no drafting)

Read, in order: the source chapter, `PROTOCOL.md` (§4 operational definitions, §5 pipeline, §6 chapter template), `CLAUDE.md` (publication targets), and every extraction/output file the chapter's reproducibility section names. Then produce **four** artifacts in `temp/rewrite/<slug>/`. All four are files. Do not return any of them only as a report — reports get lost, files do not.

**`claims.md` — the claim ledger.** One row per substantive claim. Flat, not hierarchical, and deliberately **not in the source's order**, because order is a drafting decision and must not be smuggled in as a source fact.

| # | Claim | Support | Reader needs it? | Why |
|---|---|---|---|---|

`Reader needs it?` is KEEP / CUT / DEMOTE. `Why` is one line. DEMOTE means the claim is true and belongs somewhere smaller — a subordinate clause, a caution, a footnote — rather than the section it currently occupies.

**`numbers.md` — the number ledger.** Every estimate, standard error, interval, count, percentage, date range, table/column reference, and citation, with where it came from in the source. This is the fidelity contract for Phase 4. Nothing may be rounded, re-derived, or recomputed.

**`outline.md` — the proposed outline.** Derived **from the claim ledger**, not copied from the source's section order. Each section is annotated with the claim numbers it carries, so deleting a section visibly shows which facts go with it. Must satisfy `PROTOCOL.md` §6, which sets the required sections.

Also report **omissions**, not just cuts: citations that appear in prose but not in the reference list, extraction data that never reached the chapter, a required §6 section that is missing. A screen that only subtracts will miss these. (A.10 v4 caught a Cummins reference absent from the source's reference list; the DOI was sitting in the project's own retrieval manifest.)

**The highest-value findings come from reading the chapter against the project's own data, not from reading the chapter.** The first pilot of this skill produced its best result that way: the risk-of-bias assessment existed for every study in `extraction/*-risk-of-bias-*.csv` and appeared nowhere in the chapter, and the pattern ran opposite to the chapter's conclusion — the two LOW-risk designs both returned null effects, while every study reporting a negative effect was rated SERIOUS. No prose review can find that. So open the extraction and output CSVs and check, at minimum:

- risk-of-bias ratings per study, and whether the pattern across ratings supports or undercuts the verdict
- estimates, sample sizes, and first-stage magnitudes present in the data but absent from the chapter
- study periods against the target phenomenon's window
- settings the protocol requires be flagged (e.g. §2 on policy-constrained fertility regimes)
- every §6-required section, present or absent
- author lists, years, and titles against the retrieval manifest and approved-papers table

**Separate questions from fact-checks.** A discrepancy with one correct answer (a year that differs between two files, an author list that does not match the manifest) is not a question. Record it in `numbers.md` as a fact-check to resolve during drafting, and keep the eight question slots for genuine decisions.

**`questions.md` — the Phase 2 questions.** Written as a file in Phase 1, contents specified under Phase 2 below. This is the primary deliverable of the whole screen; the ledgers exist to support it.

### Phase 2 — Questions to the PI

Surface **at most eight** questions, and only ones the PI must decide. Not style, not phrasing — decisions that change what gets written. The types that have actually mattered:

- **Category error.** "Catch-up is presented as a fourth channel, but it delays no birth. Demote to a caution?"
- **Scope.** "Sections 6 and 8 review six studies the chapter has already said do not test the hypothesis. Cut to one paragraph?"
- **Blur.** "Channels 1 and 2 look like the same mechanism. Distinguish them, or say the data cannot separate them?"
- **Framing.** "Is there a simpler way to state the wrong-generation problem?"
- **Conflict.** "Cigno and Rosati report ~10%, Shanan reports 8%. Second study, or a review relying on Shanan?"
- **Policy.** "PROTOCOL.md §4 sets a 10% significance threshold. Report the share against it, or just report the share?"

Present the questions and **stop**. Do not draft while waiting.

### Phase 3 — Draft

The PI edits `outline.md` and the ledgers directly: kills sections, rearranges, adds. Then invoke `/write-as` with the audience **declared, never inferred**, and draft against the approved outline, using the claim ledger as notes.

Write to `output/chapters/<slug>-pi-v<N>.md`, incrementing from the highest existing version. Never overwrite a prior version. If the PI has marked up a version inline, that file keeps an `-AM` suffix and is the specification.

### Phase 4 — Verify

Run in this order. Numbers first, because they are the only unrecoverable failure.

1. **Numeric fidelity, hardest gate.** Every entry in `numbers.md` appears in the draft, exactly. Nothing new appears that is not in the ledger or traceable to a named project data file.
2. **Citations.** Every prose citation carries a year on first mention and matches the reference list.
3. **Tells.** Clefts (`is what|are what|was what|were what|^What |\. What`) at zero outside reference titles; no announce-then-state sentence; no anthropomorphic inanimates; no team names (`Alexandra|Shravan|Anup|RA-approved|\bRA\b`) at zero; em-dash under the register cap.
4. **Length.** Report the delta against the prior version. Accessible is not verbose; a rewrite that grows needs a reason.
5. **Audience.** No explanation of a concept the declared reader already holds.

Then hand to `/voice-check` for the full Layer 0 screen.

## Guardrails

**Limitations survive the filter, always.** In a systematic review the caveats, null results, and identification failures *are* the product. A screen optimizing for "what does the reader need" will quietly strip the exact material that makes the work credible. Limitations, nulls, and failures to identify are never tagged CUT. If anything they get stated more plainly.

**Numeric fidelity tightens under this workflow, it does not relax.** Rewriting a document fails by copying it; composing from notes fails the opposite way, by letting numbers drift. That is why the number ledger exists and why Phase 4 checks it before anything else.

**The screen reports omissions as well as cuts.** See Phase 1.

**Never name the team in reader-facing prose.** Attribute to the review or the search. Anything genuinely aimed at collaborators goes in an explicit `[Note to co-authors: ...]` block.

**Never describe methodology the project has not run.** No future PRISMA phases, no protocol stages the reader has no reason to track.

## Audience

The declared reader for this review is a **smart undergraduate economics major**. He knows standard errors, confidence intervals, statistical significance, and what a meta-analysis pools. He does not know the economics of fertility, this literature, or anything about our pipeline.

State the implication of a statistic, not the statistic. Explain demography, evolutionary biology, and the identification problem specific to a design. Do not explain econometrics.

`PROTOCOL.md` §5 stage 13 sets the operative test: any passage that would not make sense to that reader is a defect.

## Hard NOs

- Do not draft in Phase 1. The screen produces ledgers and questions, nothing else.
- Do not build the outline by summarizing the source's section headings. Derive it from the claim ledger, or the anchoring problem returns in compact form.
- Do not proceed past Phase 2 without answers. The questions are the point.
- Do not silently fix an inconsistency found in the source. Carry the source's version and raise it as a Phase 2 question.
- Do not overwrite a prior version or a `-AM` markup file.

## Related

- `/write-as` — Phase 3 drafting, with the audience declared.
- `/voice-check` — the Layer 0 screen after Phase 4.
- `/file-voice-ticket` — file any new tell found along the way.
- `PROTOCOL.md` §5 stage 13 (readability gate), §6 (required chapter sections).
