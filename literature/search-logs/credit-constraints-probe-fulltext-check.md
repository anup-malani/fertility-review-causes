# Full-text check on the composite/savings probes — C.3.e

**TICK-077 · 2026-09-01 · Shravan**
Scripts: `280_c3e_probe_retrieval.py`, `281_c3e_probe_outcome_scan.py`, `282_c3e_scan_control.py`
Outputs: `credit-constraints-probe-retrieval.json`, `credit-constraints-probe-outcome-scan.json`,
`credit-constraints-control-{retrieval,outcome-scan}.json`

---

## Why

279 found that none of the microcredit RCTs, savings-access experiments or branch-expansion studies is
reachable by an exposure × fertility query, because none mentions fertility in its abstract. That is
either the composite stratum being empty — the most consequential thing this chapter could find, since
those are the designs Ruling 1 rests on — or a fertility outcome sitting in a table whose abstract
never advertises it. Abstract indexing and full-text tables fail for unrelated reasons, so the full
text is a genuinely independent channel. A search null is worth something only when the channels do
not fail together.

## Retrieval: 6 of 10

| Rung | Found a URL | Actually fetched |
|---|---|---|
| `oa_self` (the record itself) | 2 | 1 |
| `oa_twin` (working-paper / preprint twin) | 8 | 5 |

**The twin rung did almost all the work — 5 of the 6 fetches.** The published record is usually the
closed one. Two counters per rung, because a rung that finds eight URLs and fetches five is not the
same as a rung that finds none.

**And the twin set was itself larger than the snowball first reported.** `?` and `!` inside a *quoted*
filter value return a **silent zero** — valid `meta`, no error, an absence that is not one. Seven of
this chapter's 26 seeds carry a `?` in the title (*Do Rural Banks Matter?*, *The Miracle of
Microfinance?*, *More Credit, More Babies?*) and **every one of them returned zero twins**. This is
worse than the known `search=` wildcard refusal, which at least returns an error body. After stripping
the character: twins for **16** seeds rather than 12, pool 3,976 rather than 3,810, and **870 records
(22%) reachable only through a twin**. Banerjee's OA preprint twin — 944 citations — appeared only
after this fix, and is one of the six texts scanned below.

### The four not retrieved, split by cause

A blocked route is not a paywall, and lumping them as "unavailable" hides the fix.

| Study | Cause | Handoff |
|---|---|---|
| Attanasio et al. (Mongolia) | open URL, HTTP 403 from bot defence | **browser-job** |
| Bruhn and Love (Mexico) | open URL, HTTP 403 from bot defence | **browser-job** |
| Guinnane (credit cooperatives) | no open copy at any rung | **proxy-job** (Zotero + UChicago) |
| Prina (savings accounts) | no open copy at any rung | **proxy-job** |

## The scan, and the control that makes it believable

The question is not whether the word "fertility" appears — it is whether a fertility or birth variable
is on the left-hand side of an estimate. So the bibliography is cut before scanning (a cited paper with
"fertility" in its title is not an outcome), every hit is emitted with context for a human read, and
hits in table or outcome-list context are counted separately from prose.

**Result on the six probes: zero.**

| Study | Outcome-vocabulary hits | In table / outcome-list context |
|---|---|---|
| Angelucci et al. (Compartamos) | 0 | 0 |
| Banerjee et al. (Miracle of Microfinance) | 1 | 0 |
| Burgess and Pande (rural banks) | 0 | 0 |
| Crépon et al. (Morocco) | 0 | 0 |
| Dupas and Robinson (Kenya savings) | 0 | 0 |
| Rosenzweig and Stark (consumption smoothing) | 1 | 0 |

Both non-zero hits are false positives read by hand: "purchasing power **parity**" and "place of
**birth**". Across roughly 450,000 characters of body text there is not one fertility or birth outcome.

**A detector that fires on nothing is indistinguishable from a broken detector**, so the same code path
was run on controls known to estimate a fertility outcome:

| Control | Hits | Strong | Sample context |
|---|---|---|---|
| Cumming and Dettling (ReStud) | 175 | 17 | *"each 1 percentage point drop in the policy rate increased birth rates by 2%"* |
| Dettling and Kearney (JPubE) | 243 | 15 | *"the main dependent variable of interest: fertility rates"* |

The controls light up and classify correctly. The null is about the probes, not the scanner.

## What this establishes, and what it does not

**Establishes.** Six of the ten best-identified composite and savings-access designs — the staggered
branch-expansion experiment, three of the four microcredit RCTs, and a randomised savings-access
experiment — do not estimate a fertility outcome anywhere in their full text. They measure business
investment, profits, consumption, poverty, food consumption and entrepreneurship. Two independent
channels, abstract indexing and full text, now agree, and they fail for unrelated reasons.

**Does not establish.** Four remain unchecked, and their status is genuinely unknown rather than
negative. The finding is therefore **6 of 10 checked, 0 positive**, not "the cell is empty" — a
refusal counted as a zero is how a confident negative gets manufactured.

**The consequence if the remaining four come back negative too.** `PRIMARY_COMPOSITE_ACCESS` is empty.
The composite stratum was the reason C.3.e is one chapter and not two: it is the class of variation
that moves saving and borrowing together and cannot be allocated to either arm. If nothing in it
estimates fertility, then the sign-flip question — does financial development raise or lower fertility,
and does the net sign turn with the level of development — **has no direct evidence**, and the verdict
is UNEVALUATED with GRADE **No evidence**, never VERY LOW and never NEGLIGIBLE. Ruling 1 still stands
on its own logic: the arms remain unpoolable and the chapter remains one chapter. What changes is that
its central question would be recorded as unanswered by the literature rather than answered weakly.

## Next

1. The four-study handoff above: two browser-jobs, two proxy-jobs. Until they are read, the composite
   cell is *unresolved*, not empty.
2. A second channel on the same question, independent of these ten: search the frame for any study
   pairing a financial-access exposure with a fertility outcome. One boundary-spanning design would
   carry the stratum, and hunting for it beats counting the ones that failed.
