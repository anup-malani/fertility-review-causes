# Stage 6 prep — full-text extraction — art-access-fertility-recovery (A.17)

> **PROVISIONAL. This runs on 33 of 131 wanted records (25%).** 67 more are blocked-but-open (a browser, no institutional access) and 31 need a proxy. **Job A1 — the counterfactual set the chapter's headline number is conditional on — is 2 of 14 in hand.** Every downstream file is keyed on the OpenAlex id and skips work already done, so this re-runs cheaply when the rest arrive. A provisional pass that cannot be cheaply redone becomes the final answer by default.

**33 of 33 PDFs yielded a usable text layer.**

## Extraction quality, measured

A PDF yielding under 200 characters per page is a SCAN, not a text layer. Screening one from extracted text produces a confident 'nothing found' on a paper that says plenty, so those records are flagged `NEEDS_OCR` and excluded from the screen rather than screened badly.

| id | job | pages | chars | chars/page | tool | readable |
|---|---|---|---|---|---|---|
| `W4206510889` | A3 | 31 | 51,794 | 1,671 | pdftotext | yes |
| `W1860640930` | A2 | 53 | 110,498 | 2,085 | pdftotext | yes |
| `W2058178715` | A2 | 47 | 99,792 | 2,123 | pdftotext | yes |
| `W3210979915` | A5 | 37 | 83,112 | 2,246 | pdftotext | yes |
| `W2765482846` | A5 | 44 | 118,040 | 2,683 | pdftotext | yes |
| `W2909656495` | A5 | 28 | 76,530 | 2,733 | pdftotext | yes |
| `W2959688822` | A2 | 13 | 38,336 | 2,949 | pdftotext | yes |
| `W4397049710` | A3 | 18 | 55,641 | 3,091 | pdftotext | yes |
| `W4390964890` | A3 | 16 | 51,432 | 3,214 | pdftotext | yes |
| `W4319939934` | A3 | 22 | 70,937 | 3,224 | pdftotext | yes |
| `W3115571668` | A2 | 24 | 80,885 | 3,370 | pdftotext | yes |
| `W7160175956` | A5 | 15 | 52,126 | 3,475 | pdftotext | yes |
| `W2888653606` | A3 | 12 | 46,256 | 3,855 | pdftotext | yes |
| `W2566343964` | A2 | 28 | 109,937 | 3,926 | pdftotext | yes |
| `W7169859806` | A3 | 13 | 54,217 | 4,171 | pdftotext | yes |
| `W2429169488` | A2 | 3 | 15,871 | 5,290 | pdftotext | yes |
| `W2899333608` | A4 | 11 | 59,007 | 5,364 | pdftotext | yes |
| `W4297464366` | A2 | 17 | 91,925 | 5,407 | pdftotext | yes |
| `W4415618346` | A1 | 9 | 49,847 | 5,539 | pdftotext | yes |
| `W4408117139` | A5 | 16 | 95,429 | 5,964 | pdftotext | yes |
| `W2571030681` | C | 9 | 55,522 | 6,169 | pdftotext | yes |
| `W3191732024` | A2 | 12 | 76,104 | 6,342 | pdftotext | yes |
| `W4393989606` | A2 | 12 | 76,453 | 6,371 | pdftotext | yes |
| `W2134649289` | A2 | 15 | 96,346 | 6,423 | pdftotext | yes |
| `W4417321594` | A2 | 7 | 47,470 | 6,781 | pdftotext | yes |
| `W4414889755` | A4 | 14 | 95,881 | 6,849 | pdftotext | yes |
| `W4213171919` | C | 24 | 170,616 | 7,109 | pdftotext | yes |
| `W2284249410` | A1 | 8 | 56,972 | 7,122 | pdftotext | yes |
| `W4383264299` | A3 | 11 | 78,761 | 7,160 | pdftotext | yes |
| `W3200409296` | A4 | 8 | 61,367 | 7,671 | pdftotext | yes |
| `W3092390609` | A5 | 13 | 119,732 | 9,210 | pdftotext | yes |
| `W4387472984` | A3 | 8 | 93,435 | 11,679 | pdftotext | yes |
| `W2997596347` | A3 | 38 | 597,882 | 15,734 | pdftotext | yes |

## Readable records by job

| job | readable |
|---|---|
| `A1_COUNTERFACTUAL` | 2 |
| `A2_IDENTIFIED` | 11 |
| `A3_SHARE` | 9 |
| `A4_P5_CONVERSION` | 3 |
| `A5_P6_BEHAVIOUR` | 6 |
| `C_EXPOSURE_SERIES` | 2 |

## What the full-text screen is being asked

Relevance was settled at title/abstract. Full text exists to answer three things the abstract could not, each recorded as a field:

1. **`arm_resolved`** — the routing D2 left at `cannot_tell` for 14.4% of records. Decided in the methods section, which is why it needed full text.
2. **`counterfactual_treatment`** — *the field this chapter exists to fill.* For every arm-1 record: `none_stated` / `assumed_zero` / `partial` / `estimated`. The DISTRIBUTION of this field across arm 1 is the chapter's central result, and it is a property of the literature rather than an opinion about it.
3. **`reported_quantity`** — the number the paper reports, verbatim, with units and denominator. A.12 showed what happens when a chapter carries a number whose denominator nobody checked.

Each worklist record carries located excerpts for four probes — counterfactual language, identification language, a reported quantity, and a denominator — so the screener reads the paper's own sentences instead of searching from scratch. **The probes are a reading aid and never a verdict: a probe returning nothing is not evidence that the paper says nothing.**

