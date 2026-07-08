# Tier-B estimand-tag spot audit - old-age-security-pension-crowdout

Hardens the residual the canonical workflow flags on PI critique #1 (§7, move 3): the 247 Tier-B estimand tags behind the estimand-filtered **Recall(B) = 82.5%** were assigned by the calibrated automated gate, not RA-signed. This audits them by **double-screening** - an independent second reader re-tagged the sample blind to the automated cell (same rubric), and the group-level disagreements were RA-adjudicated.

## Design

- **Census of the adjudicable stratum:** all **99** abstract-bearing Tier-B papers audited (a real re-read is possible, so no sampling noise).
- **Sample of the ceiling:** a fixed-seed **30** of the 148 title-only papers, where both the auto-tagger and the auditor infer the estimand from a title alone - agreement there measures tagger *consistency*, not correctness.
- Weighted toward THEORY and PRIMARY, the two cells the 82.5% turns on. Total audited: **129 of 247** (52%).

## Agreement and kappa

| Stratum | n | auto-vs-audit agreement | Cohen's kappa |
|---|---|---|---|
| **Abstract census** (audit = adjudicated ground truth) | 99 | 92.9% | 0.84 |
| Title-only (auto-vs-reader, no ground truth) | 30 | 83.3% | 0.67 |
| memo: abstract census, auto-vs-reader (pre-adjudication) | 99 | 92.9% | 0.84 |

On the adjudicable stratum the automated 3-way routing (PRIMARY / THEORY / OFF) agrees with the RA adjudication on **93%** of papers (kappa 0.84, 7 corrections in 99). Title-only agreement is lower (83%, 5 of 30) and is a *consistency* figure, not an error rate - neither label is anchored to an abstract.

## The PI's question: does the THEORY routing leak?

The specific worry was that automating the tags could misroute empirical PRIMARY studies into the THEORY stream (deflating the recall denominator) or vice versa. On the abstract census:

- **THEORY -> PRIMARY leakage: 0 of 67 abstract-THEORY papers.** No formal-model tag concealed an empirical OAS->fertility estimate; the THEORY routing holds where it can be checked. (The 2 THEORY->PRIMARY flips in the full sample are both title-only guesses, carried in the band below.)
- **PRIMARY precision: 9 of 11 abstract-PRIMARY tags survive adjudication.** The 2 that fall are not theory leaks but off-cell empirics the gate over-admitted: a critique-comment (`W2093837235`) and a wrong-channel LTCI study (`W4409334223`, fertility up via care-burden relief - the Eibich-Siedler/Ilciukas class the PI himself flagged). Correcting them *tightens* the pooling set.

**Systematic minor inconsistency found.** Auto filed 5 abstract-bearing *formal models* under an OFF-outcome cell (e.g. an OLG growth model tagged `OFF:outcome-not-fertility`) instead of THEORY. This never touches the PRIMARY denominator (both are excluded), but it means the automated '65% theory' share is if anything *under*-stated - more of Tier B is theory than the auto tags said, which only strengthens the 'Tier B is mostly theory' finding.

## How the 82.5% moves under the audit

Estimand-filtered Recall(B), fixed query (Nf=Np=30), PRIMARY membership corrected by the audit:

| PRIMARY denominator | Recall(B) |
|---|---|
| auto (baseline, reproduces 36b) | 82.5% (47/57) |
| **audit-corrected** (drop the 2 confirmed off-cell) | **81.8% (45/55)** |
| robustness: keep the debatable LTCI paper in PRIMARY | 82.1% (46/56) |
| title-only sensitivity envelope (if the 5 title-only flips go the auditor's way) | 81.8% - 83.0% |

Removing the two confirmed off-cell papers moves the estimand recall from 82.5% to **81.8%** - down 0.6pp, well inside the title-only band. It moves *down* rather than up only because both removed papers were themselves query-recoverable (they name pensions and fertility in their titles), so dropping them removes two easy hits along with two off-cell studies - a wash for the recall level. The headline finding is that **the audit confirms the 82.5% rather than overturning it**: the number is stable to <1pp under a 52% audit. The audit's real payoff is *precision*, not the recall level - the pooling set is now two off-cell papers cleaner. The title-only band brackets the residual uncertainty from the 148 papers no abstract can adjudicate.

## Bottom line

The automated Tier-B tags survive the audit: **93% agreement (kappa 0.84) on the adjudicable stratum, no THEORY->PRIMARY leakage, and the only corrections tighten rather than inflate the pooling set.** The estimand-filtered Recall(B) is confirmed at ~82% (band 81.8-83.0%). The residual the workflow named is now closed on the abstract-bearing papers; the irreducible uncertainty is the 148 title-only records, which is the pilot's known identifiability ceiling, not a tagging defect. Two data-hygiene notes for the clean run: the second readers independently re-flagged several **corrupted/injected abstracts** (organic-chemistry, speech-processing, and Shakespeare text mis-joined onto pension papers) - the same ghost-citation contamination the pilot's evaluation §5 caught - so the abstract-or-live-DOI gate should run before re-tagging.
