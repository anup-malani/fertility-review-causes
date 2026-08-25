# Stage 5 fetch — art-access-fertility-recovery (A.17)

**33 of 131 retrieved (25%).** Files land in `literature/pdfs/art-access-fertility-recovery/` under the house naming convention and are gitignored.

## Yield per rung — measured, not assumed

The standing finding is that rung order is chapter-specific. B.6 built its recovery around PMC; on A.12's demography literature PMC returned zero while the free `locations` sweep did all the work. **A.17 was predicted, before this run, to be the first chapter where PMC pays** — jobs A4 and A5 are clinical, which is PMC's coverage, and they have the worst OA rates. The table below settles it either way.

**Two columns, and the difference between them is the finding.** `found a URL` is whether the rung located a candidate; `fetched` is whether that candidate returned PDF bytes. A rung that finds URLs which are then blocked by a publisher's bot defence is a LIVE rung being defeated downstream — retiring it on a zero in the second column would be refusals-read-as-zeros in retrieval costume.

| rung | found a URL | fetched | cost |
|---|---|---|---|
| `cached` | — | 33 | free (already on disk) |

| failure class | records | meaning |
|---|---|---|
| `0_best_oa` | 66 | **0** | free — already in hand from 192_ |
| `1_other_locations` | 40 | **0** | free — one API call already made |
| `2_citation_meta` | 4 | **0** | one landing-page request per record |
| `3_pmc` | 27 | **0** | one id-conversion request per record |
| `4_unpaywall` | 65 | **0** | one API request per record |

| `FAILED_route_blocked` | 67 | a 200 carrying HTML — the route is blocked, the paper is not necessarily closed; these go on a RETRY list, not to a human with a proxy |
| `FAILED_no_route` | 31 | no open route found at any rung; these are the library wantlist |

## Retrieved, by job

Read this by row. The jobs are not interchangeable: A1 is the counterfactual set the chapter's headline number depends on, and A2 is the identified evidence that no other route can recover.

| job | retrieved | wanted | rate |
|---|---|---|---|
| `A1_COUNTERFACTUAL` | 2 | 14 | **14%** |
| `A2_IDENTIFIED` | 11 | 33 | **33%** |
| `A3_SHARE` | 9 | 25 | **36%** |
| `A4_P5_CONVERSION` | 3 | 11 | **27%** |
| `A5_P6_BEHAVIOUR` | 6 | 16 | **38%** |
| `B_NO_ABSTRACT` | 0 | 27 | **0%** |
| `C_EXPOSURE_SERIES` | 2 | 5 | **40%** |

| **total** | **33** | **131** | 25% |

