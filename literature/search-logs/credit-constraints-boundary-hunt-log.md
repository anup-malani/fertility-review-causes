# Hunting a boundary-spanning design — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Script: `283_c3e_boundary_hunt.py` ·
Output: `credit-constraints-boundary-hunt.json`

---

## Result: the composite stratum is NOT empty

Ten hand-picked composite designs, six read in full, zero fertility outcomes — and the reasonable
next inference was that `PRIMARY_COMPOSITE_ACCESS` is empty. **That inference was wrong**, and one
query found it out. Counting the studies that failed was the weak version of the question; the strong
version is whether *any* study puts a financial-access exposure and a fertility outcome in the same
identified design.

Four candidates, at abstract level, none yet read in full:

| Study | Design | Exposure | Outcome | Channels |
|---|---|---|---|---|
| **Desai and Tarozzi 2011, *Demography*** | **randomized field experiment**, areas randomly allocated across credit / family-planning / control arms | credit access, crossed with family planning | contraceptive use, **fertility**, family-size preferences | both |
| Steele, Amin and Naved 1998 | quasi-experimental panel, pre-intervention measures used against selection | women's savings and credit groups | contraceptive use, **fertility** | both |
| Küchler 2012 | difference-in-differences with an instrument, panel | microfinance participation, Bangladesh | **fertility** | both |
| Lan, Pan and Yu 2023, *Applied Economics* | IV, provincial index | digital financial inclusion | fertility **intentions** | term only |

**Desai and Tarozzi is the one that could carry the stratum.** It is a randomised allocation across
arms that cross credit provision with family planning, reported in a demography journal, with fertility
among the stated outcomes. If a credit arm is separately identified from the family-planning arm, it is
a clean identified estimate of a composite financial-access exposure on fertility — the exact cell that
looked empty an hour ago. Whether that arm exists is a full-text question and is **not** settled here.

## Why the earlier reading nearly stuck, and it is a lesson about the anchors

The ten probes were the famous microcredit and financial-access papers: the 2015 *AEJ: Applied*
microcredit symposium, Burgess and Pande, Dupas and Robinson, Bruhn and Love. They were chosen as
*designs that would be ideal if they measured fertility*. They do not measure it — and the literature
that does measure it is a different literature, sitting in *Demography* and development journals, with
smaller and less celebrated designs.

**I anchored on design celebrity rather than on the estimand.** The right question was never "which are
the best financial-access designs" but "who estimates this exposure against this outcome".

**The channel split is the diagnostic, and it is stark.** Of 119 triage hits: **112 term-only, 2
provenance-only, 5 both.** The provenance channel — a 3,976-record snowball built from those same ten
anchors and their neighbours — found almost none of this literature, because snowballing from the wrong
ten reaches more of the wrong ten. Overall channel overlap was 23 records out of 6,018. A provenance
channel inherits its anchors' blind spot, and cannot be used to confirm a null the anchors caused.

This is why the two channels had to fail for unrelated reasons. They did: one is citation provenance,
the other is term retrieval, and only the term channel could see past the anchor set.

## Bounds on this triage

- **It is a triage, not a screen.** 119 hits ranked by citation, scored on title and abstract. There is
  real noise in it: *Do Remittances Promote Fertilizer Use?* (soil fertility — the known homonym),
  *World Development Indicators 2001*, an algorithmic-fairness paper. The four above were read by hand.
- **1,463 of the 6,018 records carry no abstract at all**, so the scorer is blind to them. The cell's
  status rests on what the abstracts could show; a fifth candidate may sit in that unlit fraction.
- **1,548 records pair a composite exposure with a fertility outcome** before the identification filter.
  The screen, not this triage, decides how many are real.

## Retrieval: all four blocked

| Study | Cause | Handoff |
|---|---|---|
| Desai and Tarozzi 2011 | open Duke UP PDF URL, HTTP 403 bot defence | **browser-job** |
| Steele et al. 1998 | open Population Council URL, HTTP 403 bot defence | **browser-job** |
| Küchler 2012 | no open copy | **proxy-job** |
| Lan et al. 2023 | no open copy | **proxy-job** |

Added to the four already outstanding from `280`, the human-retrieval handoff is now **eight studies:
four browser-jobs and four proxy-jobs**. Two of the browser-jobs — Desai and Tarozzi, Steele — are now
the highest-priority items in the chapter, because they decide whether the composite stratum has an
identified estimate at all.

## Status changes

- `PRIMARY_COMPOSITE_ACCESS`: **candidates exist** — no longer "may be empty". Not yet "populated":
  nothing has been read in full or extracted.
- The sign-flip question that made this one chapter rather than two now has **at least four possible
  sources of direct evidence**, where an hour ago it had none.
- Ruling 1 is untouched and was never contingent on this: the arms remain unpoolable.

## Next

1. The eight-study handoff, Desai and Tarozzi first.
2. Re-seed a snowball round 2 from the four new candidates. They come from a literature the anchor set
   could not see, so their citation neighbourhood is unexplored — and unlike round 1 it will not be
   dominated by business-outcome microcredit work.
3. Fold the composite exposure terms this hunt used but the production query lacks (`banked`,
   `unbanked`) into the frame, scored on gold recovered as before.
