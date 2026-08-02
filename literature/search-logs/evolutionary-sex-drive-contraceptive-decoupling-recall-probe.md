# A6c production query + recall probe — evolutionary-sex-drive-contraceptive-decoupling

Production query refit on full gold at CV breadth Nf=10, Np=20. Local recall is budget-free (compiled query vs gold's cached title / title+abstract); universe counts are 1 cheap OpenAlex request each.

## Local recall — how much does abstract matching rescue?

| basis | overall | Recall(A) | Recall(B) | rare-core |
|---|---|---|---|---|
| title only | 44.1% | 50.0% | 43.5% | 23% (3/13) |
| **title + abstract** | **79.7%** | 80.0% | 79.6% | 92% (12/13) |

Abstract matching lifts overall recall 44% → **80%** and the rare decoupling/desire core 23% → **92%**.

## Live universe counts — the budget cost of abstract matching

| operationalization | universe (meta.count) |
|---|---|
| `title.search` | 45,896 |
| `title_and_abstract.search` (full query) | **614,182** |

## The fork (data-driven) — RESOLVED: bank the probe, defer the pull

- `title.search`: faithful to the title-only CV; 45,896 universe; but caps recall at ~44% (misses B.1's outcome-only-title gold).
- `title_and_abstract.search`: recovers the abstract-only gold (80% recall) but the broad cause singles (status/mating/evolutionary/motivation/reproductive) inflate the universe to **614k**.
- **Tightening to phrases does NOT rescue the trade-off** (measured offline): a phrase-heavy cause block that drops the broad singles falls to **61% overall recall / 38% rare-core** — because the broad singles that drive recall are precisely the ones that explode the abstract universe. This tension is **intrinsic to B.1**: its empirical vocabulary (status, mating, reproductive success, evolutionary, motivation) is ordinary social-science/biology language, so high abstract recall and a small universe are mutually exclusive here. A reportable finding, not a query defect.

## Resolution (Shravan, 2026-07-21)

**Bank the recall probe as A6c's deliverable; do NOT pull the 614k universe.** The gold is the already-screened citation frame (95 pooling + 173 theory); the keyword query is GACS's orthogonal channel, and its recall estimate is now in hand: **title 44% / title+abstract 80% / rare-core 92%** — matching OAS's 80.6% and confirming the design-(b) forced backbone rescues the decoupling core once abstracts are matched. The citation frame is the primary corpus. Any live keyword harvest is a separate **budget-gated, bounded** task (capped `title.search` pull when the OpenAlex quota resets), exactly as OAS deferred its live pull. `production-query.json` is saved for that.

## Query (cleaned Boolean)

    (fertility OR fertilit OR birth OR "reproductive success" OR reproduction OR reproductive OR childbearing OR childbear OR "number of children" OR offspring OR "completed fertility" OR "family size" OR childless OR fecundit OR natality OR parity OR "cultural reproductive" OR "childbearing desires" OR "fertility behavior" OR "reproductive behavior" OR childlessness OR "fertility transition") AND (decoupl OR dissociat OR uncoupl OR sever OR "sex from reproduction" OR "sex without reproduction" OR "sex without conception" OR "sex drive" OR "sexual selection" OR contracepti OR "oral contraceptive" OR "the pill" OR "birth control" OR "family planning" OR motivation OR status OR motivations OR "social status" OR "problem sociobiology" OR motivational OR mating OR "motivations desires" OR ultimate OR pill OR "contraceptive pill" OR "evolutionary demography" OR "evolutionary perspective" OR sociobiology OR sexual OR fitness OR "mating success" OR evolutionary OR contraceptive)
