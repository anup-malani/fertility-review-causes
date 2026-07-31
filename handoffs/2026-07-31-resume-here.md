# RESUME HERE — fertility review, plain-language state

**Written 2026-07-31.** Branch `pi-voice-rewrites`. Read this file first. It replaces
`2026-07-29-pi-voice-rewrites.md`, which is still accurate about history but no longer about
what's left.

---

## Where things stand, in one paragraph

Five hypothesis chapters were in play. Four are finished and clean. The fifth, D.3.b on climate
anxiety, was never written, and it cannot be written until somebody reads a paper that nobody in
this project has opened. Everything else on the list is small cleanup, and three of the small items
are waiting on decisions that only the PI can make.

## The four finished chapters

| Code | What it's about | File |
|---|---|---|
| A.10 | Does keeping a girl in school longer change *her own* fertility? | `output/chapters/tempo-effects-birth-postponement-compulsory-schooling-pi-v5-memo.md` |
| B.4 | Did school laws make children less economically valuable, so parents had fewer? | `output/chapters/compulsory-education-child-economic-value-pi-v6-memo.md` |
| B.15 | Do pensions replace children as old-age insurance? | `output/chapters/old-age-security-pension-crowdout-pi-v4-memo.md` |
| B.1 | Did contraception cut sex loose from reproduction and lower births? | `output/chapters/evolutionary-sex-drive-contraceptive-decoupling-pi-v5-memo.md` |

All four now: name their hypothesis with a short label and reuse that label throughout, open Section
1 the same way, write in one voice, refer to each other by the same English name every time, and put
the credibility ratings in the summary box at the top. No em-dashes, no RA names in reader-facing
text.

---

# WHAT THE PI SHOULD DO, IN ORDER

## 1. Answer three questions yourself. About 10 minutes. Do this first.

These were emailed to the RAs on 2026-07-29 and no reply has come. You are the PI; you don't have to
wait for them. Two of the three are blocking real work.

**Question 1 — Where do the PDFs live?** Dropbox, or Git LFS (a way of storing big files inside the
code repository)? Right now 25 papers were found and downloaded somewhere, but only one PDF is on
this machine. **This blocks the last chapter.** Nothing that requires reading a paper can happen
until this is answered.

**Question 2 — Is the "10% rule" still the rule?** The protocol document
(`PROTOCOL.md` §4.2) says a cause counts as "demographically significant" if it explains at least
10% of a fertility change. All four finished chapters ignore that bar and just report the number
plainly, because you told them to. So the protocol and the chapters currently contradict each other.
Either drop the rule from the protocol, or put it back into the chapters. Fixing it is one paragraph
once you decide.

**Question 3 — What should files be named?** Lowest stakes. Purely tidiness.

## 2. Push the work to the server. One command.

Five days of finished work exists only on this laptop. Run:

```
cd /Users/amalani/github/fertility/fertility-review-causes && git push
```

## 3. Get one paper: Bisi, Sturm and Van Bavel (2024)

DOI `10.4054/demres.2024.51.2`, in the journal *Demographic Research*.

**Why this one matters more than anything else left.** The unwritten chapter, D.3.b, argues that
climate dread makes people have fewer children *even though they still want children just as much*.
That "even though" is the whole point of the chapter; without it the hypothesis collapses into a
different chapter that already exists. This paper ran an actual randomized experiment — it showed
people either a gloomy or a hopeful climate message and then measured whether they still *wanted*
children. Our own screening notes say the gloomy message made people want fewer children. If the
full paper says what the notes say, **the chapter's central claim is dead** and D.3.b should be
merged into D.1.a instead of written.

It is one of only two randomized studies out of 1,170 papers screened, and the current draft mentions
it once, in a subordinate clause. Nobody has read it.

Get it through the UChicago library, or say the word and the next session can try to fetch it
(*Demographic Research* is open access, so this may just work).

---

# WHAT THE ASSISTANT DOES NEXT, once you've done the above

Say "go" and these get worked in this order. None needs you except where marked.

1. **Write D.3.b, or kill it.** Needs question 1 answered and the Bisi paper in hand. The four
   screening files are ready at `temp/rewrite/climate-anxiety-eco-doomerism/`. There are 8 open
   questions in `questions-v1.md` that will need your answers partway through.
2. **Fix `PROTOCOL.md` §4.2** to match your answer to question 2. One paragraph.
3. **Voice lessons ledger.** You asked for this once the chapter edits settled. They have.
   **Does not need you.** 11 tickets are waiting at
   `/Users/amalani/UChicago Law Dropbox/Anup Malani/assistants/voice/tickets/inbox/`, and a partial
   write-up is at `/Users/amalani/Downloads/voice-system-fixes-brief-2026-07-26.md`.
   (The old handoff gave this path as `assistants/voice/tickets/inbox/`, which does not exist inside
   this repository — the real inbox is the Dropbox path above.)
4. **Two leftover technical tickets on B.1.** Both are recorded inside the chapter itself so they
   can't get lost. Neither changes any conclusion.
   - The script `source/analysis/b1_demographic_significance.py` produces a 4-row results table
     while the chapter now has 5 rows, and one of its rows describes an old number that has since
     been corrected. Fixing it requires first writing three studies into
     `extraction/evolutionary-sex-drive-contraceptive-decoupling-effects.csv`.
   - B.1 gained a new credibility rating that the 3-person rating panel never saw, because the row
     didn't exist when they met. It should go back to the panel.

---

# THE TWO BIG SUBSTANTIVE FINDINGS, so they don't get lost

These matter more than any of the writing work.

**B.1's main number reversed sign, and this is now fixed in the chapter.** The chapter used to say
that where contraception is absent, higher status strongly predicts more children (+0.19), versus a
weak relationship where contraception is present (+0.07) — exactly the pattern the theory predicts.
That +0.19 rested on a single study. Four more studies were sitting unused in the project's own
extraction file. Pooled properly they give **−0.06**, with a range from −0.16 to +0.05. So the
"before" side of the comparison that the theory needs was never actually established.

Stated as prominently as the finding itself: one study (Sorokowski et al. 2013, on the Yali of Papua
New Guinea) reports the two largest *positive* values anywhere in our data, +0.42 and +0.27. We only
have those numbers secondhand, through a review that quotes them without saying how many people were
sampled, so they carry no statistical weight and were left out. **The negative result is computed
without the strongest evidence against it.** Getting that paper would settle it. This is recorded in
the chapter as an open question.

**D.3.b may already be refuted by a paper inside its own search results.** See item 3 above.

---

# HOUSEKEEPING NOTES

- **Reviewing the recent commits:** B.4's commit (`3c5d97b`) looks enormous (165 lines changed)
  because the text was re-wrapped to a fixed line width at the same time as it was edited. The
  actual edits are about 40. To see only the real changes, run
  `git diff --word-diff 9fa3664 3c5d97b`. The other chapters' commits are small and read normally.
- **`temp/` is not backed up by git.** The D.3.b screening files live there and exist only on this
  machine.
- **Rules the work follows:** `PROTOCOL.md` §6 (what a chapter contains) and §6.1 (writing rules),
  plus `.claude/skills/rewrite-chapter/SKILL.md`. The skill's "Settled decisions" section is the
  compressed result of five rounds of your own markup and should not be reopened.
- **A rule worth keeping:** every real defect found in this project was found by a human or an agent
  *reading* the text, never by an automated search. The last audit is the clearest case — a search
  for the phrase "the hypothesis" reported 12 problems in one chapter; reading it found 22, plus a
  much worse problem the search could never have seen (one chapter referring to another chapter under
  three different names, one of which was a broken half-finished edit).
