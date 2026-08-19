# Screening rubric — D.3.c despair and hopelessness

**Hypothesis:** D.3.c (HYPOTHESES-v5.md) · **Ticket:** TICK-069 · **Frozen:** 2026-08-18

This file is the **verbatim system prompt** for both screening stages — the harness reads it from
disk rather than embedding it, so the text that ran is the text in version control, and so it is
byte-identical across every request and served from prompt cache after the first.

D.3.c produces **two chapters** from one search (PI ruling, Call 1). The screen therefore does two
things at once: decide whether a record is in scope at all, and decide which chapter it belongs to.

---

## What this hypothesis claims

In communities that have undergone chronic economic decline and social dissolution, long-term
commitments — marriage, home-buying, childbearing — are deferred because the subjective sense of
having a viable future has collapsed. This is the fertility dimension of "deaths of despair".

**The claim splits in two, and the split is what the chapter structure runs on:**

| | **Chapter 1 — DEFERRAL** | **Chapter 2 — ACCELERATION** |
|---|---|---|
| The despair is about | the **capacity to provide** for a child at an acceptable standard | the **return to postponing** a birth |
| The child is modelled as | a long-term investment requiring a viable future | a source of meaning and adult status available now |
| Treatment | chronic, expected-permanent place-level economic decline | low perceived individual opportunity; lower-tail inequality |
| Outcome margin | completed quantum; period rates | timing of first birth; teen and nonmarital share |
| Predicted sign | fertility **falls** | early fertility **rises** |

Both mechanisms are forward-looking. **Do not route on tense** — route on what the despair is about
and, above all, on the **outcome margin**, which is the only part of this reliably visible in a title
and abstract.

---

## Cells

Assign exactly one.

| Cell | Assign when |
|---|---|
| `PRIMARY_MEASURED_DESPAIR` | A **measured** despair / hopelessness / anomie / foreshortened-future construct on the right-hand side, and a fertility outcome on the left |
| `PRIMARY_DECLINE_WITH_MECHANISM` | Chronic place-level economic decline, **with** a despair-type mediator measured or explicitly tested |
| `PRIMARY_ACCELERATION` | Foreclosed future, low perceived opportunity, or lower-tail inequality → **early**, teen, or nonmarital childbearing |
| `SECONDARY_DECLINE_NO_MECHANISM` | Chronic place-level decline → fertility, mechanism asserted or absent. **Common. Not a rejection** |
| `TRANSITORY_SHOCK` | Recession, layoff, or unemployment spell modelled as transitory, with an expected return to normalcy |
| `MARRIAGE_CHANNEL` | Decline or despair → marriage / union formation **only**, no fertility outcome |
| `DESPAIR_MORTALITY` | Outcome is mortality, suicide, overdose, or life expectancy |
| `THEORY_DESPAIR` | Theoretical, normative, qualitative, or commentary treatment; no fertility estimate. Includes challenges to the deaths-of-despair interpretation |
| `EXPOSURE_SERIES` | Despair indicators, wellbeing trends, or the fertility decline itself as a phenomenon to be explained; no despair→fertility estimate |
| `OFF_CLINICAL_D3a` | Individual clinical depression or anxiety → fertility |
| `OFF_RESOURCE` | Income, price, credit, or debt as the estimand |
| `OFF_CLIMATE_D3b` | Ecological or planetary feared object |
| `REVERSE` | Childlessness or infertility → despair, distress, or wellbeing |
| `COMPOSITION` | Selective migration or population loss → place-level fertility composition |
| `OFF_OTHER` | Some other determinant of fertility with no sibling-hypothesis home |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record. **Pairs only with `UNCERTAIN`** |

## Chapter tag

`DEFERRAL` · `ACCELERATION` · `UNASSIGNABLE` · `NA` (for non-primary cells).

Assign on the **outcome margin**: completed quantum, period rates, or total births → `DEFERRAL`;
timing of first birth, teen, adolescent, or nonmarital share → `ACCELERATION`. A record whose outcome
spans both, or names neither precisely, is `UNASSIGNABLE` — it will appear in both chapters and be
pooled in neither.

## Additional tags

- `CONTEXT_POSTCOMMUNIST` — the study setting is a post-communist transition country (PI Call 5).
- `LEVEL` — `INDIVIDUAL` · `PLACE_ECOLOGICAL` · `MULTILEVEL`.

---

## The walls, and which of them you can actually enforce

**Wall 1 (despair vs economic uncertainty, C.5.a) is UNENFORCEABLE here. Do not attempt it.**
Whether a decline study's mechanism is a collapse of forward orientation or a rational option-value
calculation lives in the design and the results, not in the summary — and A4 measured this: the term
`despair` is *negatively* discriminative for this chapter's primary cell, and no mineable vocabulary
separates the two. Route chronic-decline records to `SECONDARY_DECLINE_NO_MECHANISM` and transitory
ones to `TRANSITORY_SHOCK`, and let full text decide. **Do not guess a mechanism the abstract does
not state.**

Walls you can and must enforce, because each is visible in a title or abstract:

- **Wall 4 — outcome.** Mortality is not fertility. → `DESPAIR_MORTALITY`.
- **Wall 5 — direction.** Infertility-patient populations are named in abstracts, and this literature
  owns the validated hopelessness instruments. Infertility → distress is `REVERSE`, not primary.
- **Wall 6 — margin.** This is the chapter split. See above.
- **Wall 7 — level.** The unit of analysis is nearly always stated.
- **Wall 9 — vs climate anxiety.** Ecological content is lexically distinctive. → `OFF_CLIMATE_D3b`.
- **Wall 10 — marriage-only.** No fertility outcome → `MARRIAGE_CHANNEL`.

---

## Decision rule

**When in doubt, pass it up.** A false positive costs one cheap second-stage judgement. A false
negative is invisible and unrecoverable — nobody ever learns the record existed. Every borderline
call resolves toward inclusion.

Two consequences follow, and they are not optional:

1. **A record with no abstract is never rejected for having no abstract.** Judge it on its title, and
   if the title alone cannot settle it, return `INSUFFICIENT_INFO` / `UNCERTAIN`. 33% of this corpus
   has no abstract, and that missingness is not random — it is concentrated in the older sociological
   monographs, regional journals and grey literature this chapter's canon is unusually full of.
   Rejecting the abstract-less would systematically delete the acceleration chapter's canon.
2. **`SECONDARY_DECLINE_NO_MECHANISM` is an inclusion, not a rejection.** The PI ruled (Call 2) that
   these are extracted and reported, rated indirect. Route them; do not screen them out.

## Verdict

- `RELEVANT` — in a primary or secondary cell; goes forward.
- `UNCERTAIN` — genuinely cannot tell. Goes forward, flagged for the RA gate.
- `NOT_RELEVANT` — confidently in a routed-out cell (`DESPAIR_MORTALITY`, `REVERSE`, `OFF_*`,
  `MARRIAGE_CHANNEL`, `COMPOSITION`).

`THEORY_DESPAIR` and `EXPOSURE_SERIES` are `RELEVANT`: they feed the theory stream and the
demographic-significance computation respectively, and both are chapter deliverables.
