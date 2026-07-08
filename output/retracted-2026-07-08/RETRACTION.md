# RETRACTED — de-ghost/rebuild artifacts from 2026-07-08 (rate-limit-poisoned)

These files are **retracted**. They were produced by the de-ghost run (`44`) and the first
rebuild pass (`46`) while the **OpenAlex daily budget was already exhausted (HTTP 429)**. The
verifier at the time treated a 429 (an outage) the same as a real "no result" — so it
misclassified an unknown number of **real papers as ghosts** and rejected real candidates.

**Evidence:** all 178 cached OpenAlex responses from the de-ghost run are `error: Rate limit
exceeded / Insufficient budget`. The de-ghost therefore ran effectively Crossref-only, and the
rebuild false-rejected ≥4 known-real papers (Manuelli–Seshadri QJE 2009; Boldrin–De Nardi–Jones;
Fanti–Gori; Raut–Srinivasan).

**Retracted numbers (do NOT cite):**
- de-ghosted Tier B 257→131, PRIMARY→17, "126 ghosts" — contaminated by false rejections
- honest recall 76.5% — built on the contaminated denominator
- rebuild "31 verified / 4 rejected" — Crossref-only, ≥4 false rejections

**What still holds (independent of the outage):**
- The **ghost-contamination finding itself** — established by clean OpenAlex probes taken
  *before* the budget was exhausted (35/36 no-DOI PRIMARY anchors returned a genuine count=0),
  plus the qualitative fabrication pattern. The pilot gold *is* ghost-contaminated; PRIMARY is
  the worst-hit cell. Only the exact magnitude is unknown pending a clean re-run.
- The **live corpus** (`{slug}-live-corpus.json`, 11,463 records) — pulled while OpenAlex was
  healthy; sound.

**Fix applied (`44`, `46`):** the verifier now returns FOUND / ABSENT / UNCONFIRMED and raises
`BudgetExhausted` on 429; an anchor is quarantined **only** when *both* OpenAlex and Crossref
return a real 200-response with no match. On any outage it halts-and-resumes and quarantines
nothing. Poisoned cache cleared.

**Re-run:** after the OpenAlex reset (midnight UTC), re-run `44` → `45` → `46` clean. Those
outputs supersede everything in this folder.
