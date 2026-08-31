# A.18 poolability — the >=3 test applied after stratification

Extraction rows: **60**. Usable estimates: **22**. Excluded: 38 ({'VERIFIED_BUT_SUPERSEDED': 1, 'RECLASSIFIED_OUT_OF_PREDICTED_RESPONSE': 1, 'RECLASSIFIED_OUT_OF_PEDIGREE_RESPONSE': 1, 'DUPLICATE_OF_W7169878769_DO_NOT_POOL': 1, 'NO_EXTRACTABLE_ESTIMATE': 16, 'NO_H2_REPORTS_OTHER_ESTIMAND': 17, 'DUPLICATE_OF_W4220783065_DO_NOT_POOL': 1}).


## Strata (estimand x outcome x relatedness)

| estimand | outcome | relatedness | studies | poolable |
|---|---|---|---|---|
| `h2_SNP` | `children_ever_born` | `POPULATION` | 2 | no |
| `h2_within_family` | `children_ever_born` | `WITHIN_FAMILY` | 1 | no |
| `h2_SNP_baseline` | `children_ever_born` | `POPULATION` | 1 | no |
| `h2_SNP_with_cohort_and_population_interaction` | `children_ever_born` | `POPULATION` | 1 | no |
| `h2_narrow_sense_family_effect_competing` | `lifetime_reproductive_success` | `WITHIN_FAMILY` | 1 | no |
| `h2_narrow_sense` | `time_to_first_birth` | `WITHIN_FAMILY` | 1 | no |
| `additive_genetic_path_cohort_linear_term_SPLINE` | `completed_fertility` | `WITHIN_FAMILY` | 1 | no |
| `additive_genetic_path_cohort_linear_term_QUARTIC` | `completed_fertility` | `WITHIN_FAMILY` | 1 | no |
| `h2_narrow_sense` | `children_ever_born` | `WITHIN_FAMILY` | 1 | no |
| `h2_SNP` | `age_at_first_birth` | `POPULATION` | 1 | no |
| `h2_GREML_twin_sample` | `childlessness` | `WITHIN_FAMILY` | 1 | no |
| `h2_SNP` | `reproductive_success` | `POPULATION` | 1 | no |
| `h2_by_birth_cohort_FEMALE_sibs` | `completed_fertility` | `WITHIN_FAMILY` | 1 | no |
| `h2_by_birth_cohort_MALE_sibs` | `completed_fertility` | `WITHIN_FAMILY` | 1 | no |
| `standardized_linear_selection_gradient_via_fertility_HEIGHT` | `reproductive_success` | `WITHIN_FAMILY` | 1 | no |
| `opportunity_for_selection_I_LRS_by_wealth` | `lifetime_reproductive_success` | `WITHIN_FAMILY` | 1 | no |
| `pgs_number_of_children_beta` | `?` | `?` | 1 | no |
| `pgs_variance_explained` | `?` | `?` | 1 | no |
| `pgs_fertility_beta` | `?` | `?` | 1 | no |
| `pgs_fertility_correlation` | `?` | `?` | 1 | no |
| `genetic_correlation_ADHD_AFB` | `?` | `?` | 1 | no |

**Strata meeting the >=3 test: 0.**


Applied before stratification the same evidence would have looked poolable: there are enough usable estimates in total. Stratified, they scatter across estimands that cannot be averaged — a variance component, a per-SD polygenic-score beta and a genetic correlation are three different quantities.


## Consequence for the synthesis

The chapter reports a **narrative synthesis with a stratified evidence table**, not a meta-analytic pool. That is a finding about this literature, not a shortfall in the search: 696 studies were screened, 148 reached the primary cells, and the estimates they report are heterogeneous in kind rather than merely in magnitude.

