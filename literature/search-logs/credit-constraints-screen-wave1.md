# Screen, wave 1: the two dense strata — C.3.e

**TICK-077 · 2026-09-01 · Shravan** · Scripts `293` (sheets), `294` (ingest + validation) ·
Output: `extraction/credit-constraints-screen.csv`, `credit-constraints-screen-results.json`

349 records screened at title and abstract — all 80 of `both_channels` on full abstracts, all 269 of
`snowball_r2_only` on titles with abstracts read wherever a finance and a fertility token co-occurred.
Zero validation errors: every verdict id exists on the sheet, no record routed twice, and all 349 are
accounted for (292 recorded explicitly as `OFF_OTHER_read_not_routed`, an explicit residual rather than
an absence).

## The probe's yield curve held

| Stratum | n | Primary | Probe predicted |
|---|---|---|---|
| `both_channels` | 80 | **20 (25.0%)** | ~23% |
| `snowball_r2_only` | 269 | **6 (2.2%)** | ~4% |

A 40-record probe per stratum predicted the full screen to within two points on the dense stratum. That
is the case for probing depth rather than screening sequentially, and it means the `frame_only` (~6%)
and `snowball_r1_only` (~1%) estimates can be planned against.

## The primary pool: 26 records

| Cell | n |
|---|---|
| `PRIMARY_COMPOSITE_ACCESS` | 19 |
| `PRIMARY_BORROW_TERMS` (Arm B) | 4 |
| `PRIMARY_SAVE_INSURE` (Arm S) | 3 |

Plus `THEORY` 9, `REVERSE` 1, `MECHANISM_NO_FERTILITY` 3, `REVIEW_TO_MINE` 1, and 17 routed to
neighbouring chapters.

**The composite cell, empty this morning, is now the largest cell in the chapter.** Nineteen records,
mostly microcredit-and-contraception studies from Bangladesh, Ghana, Indonesia and Kenya, plus four
aggregate financial-development papers that will sit in a secondary pool on design grounds.

**The FDT cell is populated, and by two records rather than one.** Alongside *Fertility and Financial
Development: Evidence from U.S. Counties in the 19th Century*, the screen found **"Rainfall risk,
fertility and development: evidence from farm settlements during the American [frontier]"** — children
as a buffer stock of labour against rainfall risk. That is the insurance motive, in an FDT-era setting,
with a risk shock as the source of variation. The scope memo had called this cell the thinnest and most
valuable if it existed; it now has two members and both are Arm S.

**Arm S remains the thinnest arm — 3 primary records — and that is a finding, not an artefact.** Arm B
has 4 from this wave plus the inherited C.2.c set and Dettling and Kearney 2025; Arm S has these three
plus Cain and Pörtner. If the ratio survives the remaining waves, Arm S's GRADE will rest on very
little, and PM in particular may end UNEVALUATED.

## Wall 1 is load-bearing, confirmed at volume

**Fifteen records routed to C.3.c** — the old-age-security motive, from Nugent-era theory through to the
2022 *AEJ: Economic Policy* Namibian social-pension study. That is 19% of `both_channels`, and it is the
single largest off-routing in the chapter. The wall drawn in the scope memo on the question *which risk
is insured* is doing real work rather than dividing an empty set.

One record is flagged for revisiting: **"Old-age security motives, labor markets, and farm family
fertility in antebellum America"** is FDT-era and on Arm S's setting. It routes to C.3.c on the wall as
written, but it sits adjacent to the two FDT records above, and if C.3.c declines it, it comes back.

## One record is evidence about identification, not about the effect

**"Children as insurance revisited: impact of children on private insurance adoption"** estimates the
arrow *backwards* — children on insurance take-up, not insurance on fertility. Routed `REVERSE`. It
belongs in the risk-of-bias discussion as direct evidence that reverse causality in this literature is
real and measured, which is a stronger statement than the usual assertion that it is possible.

## Bounds

- Title-and-abstract only. Design values are hypotheses until full text: an earlier chapter carried a
  paper as an administrative allocation through three stages and it turned out to be IPTW.
- The 269-record stratum was screened on titles, with abstracts read where the token classes
  co-occurred. That is thinner than the abstract-level pass given to `both_channels`, and its 2.2%
  should be treated as a floor.
- 23% of the wider universe still has no abstract and is untouched by this wave.

## Next

1. `frame_only`, 2,271 records at ~6% — the largest remaining block of relevant work (~135 records).
2. Mine the two systematic reviews, now three with *Community-Based Financing of Family Planning*.
3. `snowball_r1_only` last, at lower depth, with a bounded blind tail sample.
