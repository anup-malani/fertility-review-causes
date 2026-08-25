# D1 deterministic ranking — art-access-fertility-recovery (A.17)

**7,589 Tier-B records in, 276 version duplicates collapsed on normalized title, 7,313 ranked.** Nothing is deleted: every record keeps its score, rank and hit lists, so the cutoff can be re-cut without re-running retrieval.

## The exposure axis is ambient and is not scored

Every prior chapter scored an exposure axis against an outcome axis and let the cross-axis AND do the work. A.17 cannot. The frame was pulled entirely from ART seeds, so ART vocabulary is everywhere: **2,948 records (40.3%) name it explicitly** and the rest are ART-adjacent by construction. Scoring it would rank the 204,210-record clinical cloud alongside the primary cell and call the result precision. `art_hits` is retained on every record for reporting and contributes zero to the score.

## What discriminates instead: two arm signatures, scored apart

| signature | definition | records | share |
|---|---|---|---|
| **ARM 2 (identified)** | ACCESS exposure x population outcome | 133 | 1.8% |
| **ARM 1 (accounting)** | COUNTING language x population outcome | 184 | 2.5% |
| Identification language | the A4-measured 4x prior for arm 2 | 252 | 3.4% |
| Elective preservation | PI call 2's cell | 49 | 0.7% |
| Wall 5 residue | preservation naming NEITHER indication | 156 | 2.1% |

The two arm signatures are scored separately and equally and their hits are kept apart on every record. Merging them would produce a ranker that cannot distinguish a study estimating a policy response from a report tabulating a share — the distinction the whole chapter turns on.

**Identification language is a bonus and never a filter.** It fires on 252 records in 7,313 (3.4%), so it can lift the identified evidence and is arithmetically incapable of demoting anything. A4 measured it at 1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones; that is a real prior and a thin one, and it is used accordingly.

## A third of the frame has no abstract

**2,392 records (32.7%) carry a title only.** A title-only record cannot be screened on content at anything like the power of one with an abstract, and its `NOT_RELEVANT` would mean *not visible*, not *not relevant*. The `no_abstract` flag travels with every record so the screen buckets these as `INSUFFICIENT_INFO` rather than silently converting missing metadata into a negative verdict.

## Worklist

**Budget slice: 800** (score cutoff 16). Plus four bypasses, each carrying records read *wherever they rank*:

| bypass | rationale | n |
|---|---|---|
| `bypass_arm2_identified` | the chapter's only identified evidence, 133 records in 7,313 — a budget cutoff is the wrong instrument for a population that small | 23 |
| `bypass_arm1_accounting` | the arm that produces the headline number | 69 |
| `bypass_elective_preservation` | PI call 2's cell; an empty cell and an unread cell are identical evidence and opposite conclusions | 23 |
| `bypass_wall5_residue` | the records that cannot be routed without being read | 105 |
| **total worklist** | | **1,020** |

**On the budget.** The 800-record slice is an in-session SCREENING-THROUGHPUT limit, not a cost limit, and the distinction matters because the two point in opposite directions. Screening the entire 7,313-record frame would cost single-digit dollars batched — the standing lesson is that screen cost has never been this project's binding constraint. What bounds this run is that verdicts are produced by reading batches in-session, and 7,313 records is roughly 127 batches. **The bypasses are sized so that the budget decides only the tail: every record in either arm's candidate cell is read regardless of rank.** If a batch API key is available, the right move is to drop the slice and screen the frame entire; the ranking is retained precisely so that can be done without re-running anything upstream.

## Version duplicates collapsed (examples)

| title | kept DOI | dropped DOI | kept cites | dropped cites |
|---|---|---|---|---|
| The International Glossary on Infertility and Fertility Ca | `10.1016/j.fertnstert.2017.06.005` | `10.1093/humrep/dex234` | 1500 | 1327 |
| American Cancer Society/American Society of Clinical Oncol | `10.1200/jco.2015.64.3809` | `10.3322/caac.21319` | 1048 | 747 |
| Accelerate progress—sexual and reproductive health and rig | `10.1016/s0140-6736(18)30293-9` | `None` | 1479 | 627 |
| On the Quantum and Tempo of Fertility | `10.2307/2807974` | `10.31899/pgy6.1010` | 668 | 586 |
| Choosing Among Alternative Nonexperimental Methods for Est | `10.3386/w2861` | `10.1080/01621459.1989.10478848` | 896 | 512 |
| Fertility Preservation in Breast Cancer Patients: A Prospe | `10.1200/jco.2005.05.037` | `10.1080/14733400500247512` | 532 | 424 |
| Multiple gestation pregnancy | `10.1093/humrep/15.8.1856` | `None` | 378 | 309 |
| Fertility Preservation in Women | `10.1056/nejmra1614676` | `10.1038/nrendo.2013.205` | 853 | 309 |

## Top 25 by D1 score

| rank | score | arm | year | title | venue |
|---|---|---|---|---|---|
| 1 | 121 | **2** | 2018 | HOW DO STATE INFERTILITY INSURANCE MANDATES AFFECT DIVORCE? | Contemporary Economic Policy |
| 2 | 112 | **2** | 2015 | Assisted reproductive technology use, embryo transfer practices, and birth | Fertility and Sterility |
| 3 | 111 | **2** | 2016 | State Insurance Mandates and Multiple Birth Rates After In Vitro Fertiliza | Obstetrics and Gynecology |
| 4 | 106 | **2** | 2022 | Impact of in vitro fertilization state mandates for third party insurance  | Reproductive Biology and Endoc |
| 5 | 105 | **1** | 2025 | The contribution of medically assisted reproduction to total, age-, and pa | Human Reproduction |
| 6 | 101 | **1** | 2023 | Projecting the Contribution of Assisted Reproductive Technology to Complet | Population Research and Policy |
| 7 | 97 | **1** | 2023 | The influence of the increasing use of assisted reproduction technologies  | Scientific Reports |
| 8 | 96 | **1** | 2025 | Shifting the reproductive window: The contribution of ART and egg donation | Population Studies |
| 9 | 95 | **2** | 2011 | Utilization of Infertility Treatments: The Effects of Insurance Mandates | National Bureau of Economic Re |
| 10 | 95 | **2** | 2023 | Childbirth timing and completed family size by the mode of conception—the  | The Lancet Regional Health - W |
| 11 | 95 | **2****1** | 2026 | In Vitro Fertilization Utilization Rates and Outcomes in States With and W | Urology |
| 12 | 94 | **2** | 2009 | Did the US Infertility Insurance Mandates Affect the Time of First Birth? | SSRN Electronic Journal |
| 13 | 91 | **2** | 2009 | Infertility Insurance Mandates: Morality or Regulatory Policy? | SSRN Electronic Journal |
| 14 | 90 | **2** | 2019 | US State-Level Infertility Insurance Mandates and Health Plan Expenditures | Maternal and Child Health Jour |
| 15 | 90 | **2** | 2006 | Effects of infertility insurance mandates on fertility | Journal of Health Economics |
| 16 | 89 | **2** | 2015 | Contraception Use, Abortions, and Births: The Effect of Insurance Mandates | Demography |
| 17 | 89 | **1** | 2026 | Microsimulation reveals that medically assisted reproduction is unlikely t | Human Reproduction |
| 18 | 88 | **1** | 2020 | Latest‐Late Fertility? Decline and Resurgence of Late Parenthood Across th | Population and Development Rev |
| 19 | 88 | — | 2014 | Demographic relevancy of increased use of assisted reproduction in Europea | Reproductive Health |
| 20 | 88 | **2** | 2012 | A reduction in public funding for fertility treatment - an econometric ana | BMC Health Services Research |
| 21 | 88 | **2** | 2007 | Effects of Increased Access to Infertility Treatment on Infant and Child H | SSRN Electronic Journal |
| 22 | 84 | **2** | 2002 | Insurance Coverage and Outcomes of in Vitro Fertilization | New England Journal of Medicin |
| 23 | 83 | **2** | 2017 | Affordability of Fertility Treatments and Multiple Births in the United St | Paediatric and Perinatal Epide |
| 24 | 82 | **2** | 1998 | The economic cost of infertility-related services: an examination of the M | Fertility and Sterility |
| 25 | 82 | **2** | 2007 | Mandated Health Insurance Benefits and the Utilization and Outcomes of Inf | National Bureau of Economic Re |
