# LLM Screening Prompt — old-age-security-pension-crowdout
# Pipeline stage: between Boolean search (Stage 3) and human title/abstract screen (Stage 4)
# Model: Haiku (fast, cheap) for bulk; Sonnet for UNCERTAIN cases
# Validated: 2026-06-20 — 12/12 recall, 12/12 precision on 24-paper test set | Prompt revised 2026-06-20 (batch-2 calibration: changes 1–3) | Prompt revised 2026-06-20 (batch-3 calibration: changes 4–6)

---

## Prompt

You are screening abstracts for a Cochrane-style systematic review of explanations for fertility decline.

**Hypothesis under review:** Public pensions and formal old-age insurance reduce fertility by substituting for children as a retirement-support asset. When governments provide retirement income, the economic motive for having children (who would otherwise support elderly parents) weakens.

**Causal direction being tested:** pension/old-age security systems → fertility/childbearing decisions. This is NOT the reverse direction (fertility trends affecting pension system sustainability).

**Classify this paper as RELEVANT if it:**
- Studies whether the availability, generosity, or introduction of formal pension systems (social security, PAYG pensions, provident funds) or informal old-age support affects fertility rates, desired family size, or childbearing decisions
- Models or tests children as a savings vehicle or old-age insurance substitute (the "old-age security motive" for fertility), even without mentioning pensions explicitly
- Studies the value or cost of children as old-age support (the 'children-as-retirement-insurance' or 'old-age security motive') even if no formal pension system is mentioned — including papers analyzing parental expected benefits from children in old age, the structural value of children as old-age insurance, or sequential birth strategies aimed at securing a surviving child for old-age support
- Studies the old-age security motive through the **Value of Children (VOC)** framework or through discussions of parental or women's social and economic dependence on children in the absence of formal safety nets — papers invoking VOC that include old-age support as a component of children's value are in scope even if "pension" never appears
- Uses natural experiments (pension reforms, pension expansions) to estimate causal effects on fertility
- Analyzes cross-national or historical variation in pension coverage as a predictor of fertility change
- Develops theoretical models where old-age security arrangements determine equilibrium fertility
- Tests or extends the Becker-Barro fertility model, the Caldwell wealth-flows model, or overlapping-generations (OLG) / lifecycle models in which **fertility is an endogenous choice variable** and intergenerational transfers — formal or informal, including bequests, PAYG contributions, longevity-contingent savings, or survival-contingent child investments — enter the agent's budget constraint or utility function; structural equivalence to pension-crowdout is sufficient for RELEVANT even if no named pension policy appears
- Paper title or abstract uses **government/family crowdout language** — "government crowding out family," "state substituting for kin," "public provision replacing private intergenerational support," or close paraphrases — classify as RELEVANT and flag for human review regardless of whether "pension" appears

**Classify as NOT RELEVANT if:**
- The paper treats fertility decline as a *cause* or *context* for pension system sustainability problems rather than pension generosity as a cause of fertility change (reverse causal direction) — e.g., papers projecting pension expenditure under demographic aging, or modeling pension reform necessitated by low birth rates; when the causal arrow is ambiguous, prefer UNCERTAIN over NOT_RELEVANT
- The paper studies fertility or birth rates but the connection to old-age security or pensions is absent or only background demographic context ("fertility decline strains pension systems")
- The paper is an epidemiology or disease burden study (Global Burden of Disease, cancer, stroke, disability) that mentions TFR as a demographic variable
- The paper studies other causes of fertility change (education, female labor supply, housing, contraception) without a pension/old-age security component

**When uncertain:** lean toward RELEVANT (false negatives are more costly than false positives in this pipeline).

Title: {{TITLE}}
Abstract: {{ABSTRACT}}

Respond with exactly this format:
VERDICT: RELEVANT | NOT_RELEVANT | UNCERTAIN
CONFIDENCE: HIGH | MEDIUM | LOW
REASON: [one sentence]

---

## Validation record

**Test date:** 2026-06-20
**Test set:** 24 papers (12 RELEVANT heuristic label, 12 NOT_RELEVANT heuristic label)
**Recall (RELEVANT):** 12/12 = 100%
**Precision (NOT_RELEVANT):** 12/12 = 100%
**All verdicts:** HIGH confidence

**Key finding:** The causal-direction clause ("NOT the reverse direction") is the primary discriminating feature. It catches papers that co-mention pensions and fertility but study pension finance with fertility as a demographic input — the exact false positive category that the Boolean query cannot exclude.

**Known gray zones to monitor in production:**
1. OLG macro papers where pension design affects fertility only as a third-order equilibrium byproduct (currently: lean RELEVANT per tie-breaker instruction)
2. QQ-tradeoff papers that mention old-age security as one of several mechanisms without making it central (currently: lean RELEVANT)
3. Papers on pension reform fiscal effects that include a secondary fertility regression as a robustness check (should be RELEVANT — the prompt correctly catches these)

**Suggested re-validation trigger:** after first 500 papers screened in production, spot-check 50 UNCERTAIN verdicts and 20 NOT_RELEVANT verdicts for missed relevant papers.

---

## Workflow integration

This prompt is used in `screen-titles-abstracts.mjs` (Stage 4 of PROTOCOL.md pipeline).

Input: `literature/search-logs/{slug}.json` (output of `literature-search.mjs`)
Output: same JSON with `llm_verdict`, `llm_confidence`, `llm_reason` fields added to each paper

Routing:
- RELEVANT + HIGH → pass to human screen queue
- RELEVANT + MEDIUM/LOW → pass to human screen queue (flagged for closer attention)
- UNCERTAIN → pass to Sonnet for re-screening; if still UNCERTAIN, pass to human
- NOT_RELEVANT + HIGH → exclude (log DOI for audit)
- NOT_RELEVANT + MEDIUM/LOW → pass to human screen queue (flagged)

Prompt revised 2026-06-20 based on batch-2 calibration — changes 1–3 address demand-side OAS motive papers, OLG/Becker-Barro framework papers, and reverse-direction false positives.
Prompt revised 2026-06-20 based on batch-3 calibration — changes 4–6 add VOC-framework / women's-dependence coverage (change 4), strengthen OLG endogenous-fertility recognition (change 5), and add title-level crowdout-language rule (change 6).
