# RESUME HERE — fertility review, plain-language state

**Updated 2026-07-31, end of session.** Branch `pi-voice-rewrites`, everything pushed.
Read this file first. It replaces `2026-07-29-pi-voice-rewrites.md`, which is history now.

---

## Where things stand, in one paragraph

Four chapters are finished, clean, and consistent with each other. The fifth, D.3.b on climate
anxiety, still has no draft — and the paper that arrived this session suggests it may not deserve one.
The protocol, the shared literature folder, and the RA instructions are all settled and sent. What
remains is one real chapter decision and a handful of technical tickets.

## The four finished chapters

| Chapter | About | Tag it uses |
|---|---|---|
| A.11 | Does keeping a girl in school longer change *her own* fertility? | the own-schooling hypothesis |
| C.3.b | Did school laws make children less economically valuable, so parents had fewer? | the lost-child-earnings hypothesis |
| C.3.c | Do pensions replace children as old-age insurance? | the old-age-security hypothesis |
| B.1 | Did contraception cut sex loose from reproduction and lower births? | the delink-sex-and-reproduction hypothesis |

Files are in `output/chapters/`, named `*-pi-v<N>-memo.md`. Never overwrite a file ending `-AM`; those
carry PI markup and are the spec for the version after them.

---

# WHAT THE PI SHOULD DO, IN ORDER

## 1. Answer the eight D.3.b questions — but answer a different question first

File: `temp/rewrite/climate-anxiety-eco-doomerism/questions-v1.md`

**Read the Bisi abstract before the eight questions.** The paper is now on disk at
`fertility/fertility-review-lit/causes/D.3.b-climate-anxiety-eco-doomerism/`. Its finding, verbatim
from the abstract: *"The exposure to a pessimistic scenario increased the likelihood of low fertility
desire in both Belgian and Italian respondents."*

D.3.b's distinctive claim is that climate dread suppresses childbearing **while the desire for
children stays intact**. Bisi randomized a gloomy climate message and the desire moved. If desire is
what changes, the mechanism is preference change, which is the neighbouring chapter's mechanism, and
D.3.b has no distinctive content left.

Be precise about how far this goes. It measures desires rather than births, on 431 university
students, using a hypothetical vignette rather than real climate exposure. So it does not refute
"climate anxiety lowers fertility." It knocks out the premise that separates D.3.b from D.1.a. One
small student experiment is not decisive alone, but it is one of only two randomized designs in 1,170
screened records and it points straight at the load-bearing premise.

**So the first decision is: does D.3.b survive as its own chapter, or fold into D.1.a?** Answer that,
then the eight questions either matter or become moot.

## 2. Decide what to do about the hypothesis codes

The codes in our chapters and notes do not match the master list, and the RAs have now been told to
trust the master list and flag anything stale, so they will run into this.

| Called this in our notes | Actually this in `HYPOTHESES-v5.md` |
|---|---|
| A.10 | **A.11** — tempo effects and birth postponement |
| B.4 | **C.3.b** — child labor restrictions and compulsory schooling |
| B.15 | **C.3.c** — old-age security and pension crowdout |
| B.1, D.3.b | correct as written |

Three ways to resolve it, your call:

1. **Renumber our chapters and notes to match the master list.** Most correct, most churn.
2. **Change the master list to match the chapters.** Least churn, but the master list is the thing
   the search pipeline and the Dropbox folder names are generated from, so this fights the tooling.
3. **Drop codes from prose entirely and key everything on slugs.** Slugs have never drifted, and every
   file in the repo already uses them. Codes would survive only in `_INDEX.md` and the master list.

Option 3 is what I would pick, and it is the direction the folder builder already went, but it is a
book-organization decision rather than a technical one.

## 3. Nothing else needs you

Everything below runs without your input once you have decided 1 and 2.

---

# WHAT THE ASSISTANT DOES NEXT

Say "go" and these run roughly in this order.

1. **Resolve D.3.b** — write it, or merge it into D.1.a and record why. Needs decision 1.
2. **Write the three re-pooled studies into `extraction/evolutionary-sex-drive-contraceptive-decoupling-effects.csv`.**
   This one write unblocks three things: `b1_demographic_significance.py` can then generate the
   chapter's five rows instead of four, its stale pre-modern row stops describing a superseded number,
   and B.1's forest plot stops being stale. All three are recorded as protocol deviations inside B.1
   so they cannot get lost.
3. **Send B.1's new pre-modern rating to the three-rater panel.** The row was created this session by
   the PI's decision to rate the two halves of the status-and-reproduction claim separately, so the
   panel never saw it. Two other B.1 ratings are queued for the same panel.
4. **Process the 11 voice tickets** at
   `/Users/amalani/UChicago Law Dropbox/Anup Malani/assistants/voice/tickets/inbox/`. This is the
   voice assistant's job in its own project, not this repo's.

---

# WHAT GOT DONE THIS SESSION

For context, not action.

- **B.1's bottom-line contradiction resolved.** The status-and-reproduction claim now splits into the
  pre-contraceptive gradient and the dissociation under contraception, rated separately. The GRADE and
  verdict tables both went to five rows and agree with each other for the first time.
- **Referent audit on all four chapters.** Every chapter now names its hypothesis with a short tag and
  reuses it. Reading found about twice what grep did. The worst defect grep could never have found:
  C.3.b referred to A.11 under three different names, one of them a broken half-finished substitution.
- **The 10% significance rule is withdrawn** (`PROTOCOL.md` §4.2), with the reasoning recorded so
  nobody re-invents it. Both RAs concurred. Three chapter notes updated; no chapter text needed to
  change because they were already reporting shares plainly.
- **Shared literature folder built** at `fertility/fertility-review-lit/causes/`, shared with both RAs,
  with generated `_README.md` and `_INDEX.md`. Built by `source/build/sync_lit_folders.py` from the
  master list rather than typed, because the codes drift.
- **Bisi, Sturm and Van Bavel (2024) retrieved and filed.** See item 1 above.
- **Voice lessons ledger written** to
  `assistants/voice/context/lessons-ledger-fertility-rewrites-2026-07-31.md`.
- **RAs emailed** with the threshold decision, the filing rules, and the code drift.
- **B.1's cross-reference to A.4 corrected to A.14.** It had pointed readers at the abortion-access
  chapter when it meant coital frequency. Found by validating codes against the master list with a
  script, which is the one defect class a script catches better than a person.

---

# HOUSEKEEPING

- **Waiting on the RAs:** the email asks them to confirm they can *add* a file, not just read one. I
  could not verify through the API whether the share went out as "Can edit" or "Can view", and
  view-only would look fine while silently breaking everything. If they report they cannot write,
  re-share with edit rights.
- **`literature/pdfs/` in the repo is now redundant.** It holds one PDF that also lives in Dropbox.
  The directory is gitignored, so nothing breaks either way, but Dropbox is the home now.
- **Reviewing commit `3c5d97b`** (the C.3.b referent audit) needs `git diff --word-diff 9fa3664 3c5d97b`,
  because the file was re-wrapped in the same commit and the raw diff is four times larger than the
  real change. Every other commit reads normally.
- **`temp/` is not in git.** The D.3.b screening files and `hypothesis-codes.json` live there and exist
  only on this machine.
- **Rules the work follows:** `PROTOCOL.md` §6 (chapter structure) and §6.1 (writing conventions), plus
  `.claude/skills/rewrite-chapter/SKILL.md`. The skill's "Settled decisions" section is the compressed
  output of many rounds of your markup and should not be reopened.
- **The rule that keeps proving itself:** every substantive defect in this project was found by
  reading or by an ad-hoc measurement built for the occasion, never by the standing automated screen.
  The one exception is this session's miscoded cross-reference, which only a script would have caught.
  Use both; trust neither alone.
