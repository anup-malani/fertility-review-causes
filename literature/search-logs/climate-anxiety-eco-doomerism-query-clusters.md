# Query clusters — climate anxiety and eco-doomerism

**Hypothesis:** D.3.b (`HYPOTHESES-v5.md`) · slug `climate-anxiety-eco-doomerism`
**Stage:** A2 (cause-axis clustering) — written after the A1 scope freeze, before A3 anchor sourcing
**Status:** provisional five-family design; the operational count is confirmed or collapsed by the
post-A3 §7.2 retrieval-overlap test, not here.

---

## 1. Why cluster

Following the OAS clustering method (`old-age-security-pension-crowdout-query-clustering-method.md` §2)
and the B.1 precedent (`evolutionary-sex-drive-contraceptive-decoupling-query-clusters.md`): decompose
the hypothesis into vocabulary families so environmental psychology, demography, family sociology, and
population ethics are each searched *on their own terms*, and so the search budget is allocated across
families observably rather than spent on one broad relevance query. Union, not intersection — a paper
written in only one disciplinary vocabulary is retained, not dropped.

## 2. The effect axis (shared — held out of every overlap test)

The fertility outcome vocabulary is constant across all cause-axis families and is therefore **held
out** of the pairwise overlap computation (per `38_cluster_overlap.py`: including the shared axis would
wash every Jaccard toward 1):

- realized fertility, births, TFR, completed fertility, number of children, parity, offspring;
- **D.3.b-specific extension (load-bearing — the outcome is dominantly stated intention):** fertility
  intention, reproductive intention, childbearing intention, desire for children, intended / planned /
  ideal parity, decision to have children, voluntary childlessness, childfree, reasons for not having
  children — plus the "desire held fixed" clause (desire positive but suppressed) that distinguishes
  D.3.b from D.1.a.

The intention vocabulary is inside the *constant* effect axis by design, because per the A1 synthesis
freeze stated-intention outcomes are a first-class part of the primary synthesis (flagged as stated).

## 3. The five cause-axis families

| # | Family | Discriminative term core | Scope cell(s) | Counts toward empirical recall? | Discipline |
|---|---|---|---|---|---|
| 1 | **climate/eco-anxiety construct** (exposure spine) | climate anxiety, eco-anxiety, ecological grief, solastalgia, climate distress, climate worry, environmental worry, climate emotions, climate-change concern, climate distress | `PRIMARY_*` when paired with a fertility outcome; `THEORY` when a bare scale-validation / construct paper | Yes when paired with fertility; the bare-construct papers route to theory | environmental / clinical psychology |
| 2 | **habitability / future-for-children fear** | world uninhabitable, bringing a child into this world, "what kind of world," bleak/dangerous future, future for our children, planetary future, future generations × climate, unsafe world | `PRIMARY_HABITABILITY_FEAR` | Yes | sociology, qualitative fertility studies |
| 3 | **carbon-ethics / environmental anti-natalism** | carbon footprint of a child, carbon legacy, emissions of having children, overpopulation, antinatalism, procreative / population ethics, moral duty not to reproduce, "one fewer child," environmental antinatalism | `PRIMARY_CARBON_ETHICS`, `THEORY` (population-ethics canon) | Yes when empirical; the philosophy canon routes to theory | environmental ethics / philosophy, demography |
| 4 | **eco-doom / environmental pessimism** | doomism, eco-doom, climate doom, collapse, existential risk, apocalyptic, environmental pessimism, hopelessness about the future × climate, catastrophe | `PRIMARY_ECO_PESSIMISM` | Yes | sociology, psychology |
| 5 | **reproductive-decision / motivation under climate** (bounded — the D.1.a wall) | reproductive decision-making, childbearing decisions, motivations for childlessness, reasons for not having children, voluntary childlessness × environment — with the **D.1.a wall** (fear-suppressed desire vs positive child-free preference) | `DESIRE_INDEPENDENCE` | Yes | family sociology, psychology of fertility |

## 4. Design-time overlap read (provisional — empirical test is post-A3)

The binding §7.2 test — Jaccard ≥ 0.60 on *retrieved gold sets* — cannot run until A3 builds the gold.
What follows is the a-priori conceptual/vocabulary read that fixes the provisional count; A3's gold
confirms or collapses it.

- **1 ↔ 2 ↔ 4 (construct ↔ habitability-fear ↔ eco-doom) — the watch-triple.** These share the
  affective-dread vocabulary: a paper on eco-anxiety often also names "the future for our children" and
  a "bleak/apocalyptic" outlook, so they will pull heavily overlapping retrieved sets. Most likely to
  collapse into one operational cluster on the post-A3 Jaccard. Kept as three *search* buckets anyway,
  because they map to three distinct estimand cells the extraction must separate, and family 1 is the
  exposure spine every primary shares. *Separate at search, expect merge at budget.*
- **3 (carbon-ethics) — expected to stay distinct.** Its vocabulary is moral/philosophical
  (overpopulation, antinatalism, procreative ethics, carbon legacy), which shares little with the
  affective anxiety terms. It also carries its own theory-stream tail (population-ethics philosophy).
  The B.1 analog: family 3 played the role family 3 (carbon-ethics) plays here — a distinct vocabulary
  with its own theory tail.
- **5 (reproductive-decision / motivation) — the D.1.a wall lives here.** This is where D.1.a leakage
  enters (voluntary-childlessness and childbearing-decision papers, most of which are positive-preference
  and route away), so it needs its own bounded vocabulary and the routing wall, exactly as B.1's
  bounded contraception family carried the A.2 wall. Its "childbearing decision / voluntary
  childlessness" terms overlap the effect-axis intention extension but, held out, the family's
  distinctive content is the motivation framing.

**Provisional operational count: five vocabulary families.** Honest expectation for the post-A3 budget
count: **3** — {1+2+4} the probable affective-dread merge, {3} carbon-ethics distinct, {5}
reproductive-decision distinct. The five-way split is carried into A3 so anchor sourcing samples every
family — at least one habitability-fear, one carbon-ethics, one eco-pessimism, one climate-anxiety
construct (theory), and one reproductive-decision anchor — and the eventual search is tested on routing
across all five, plus the three off-cell decoys (D.1.a / D.3.a / C.5.a), not just topical retrieval.

## 5. Caveats

1. This is a **conceptual/vocabulary** overlap read, not the retrieval-overlap test. Two families that
   mean different things can still be one operational cluster if they pull the same papers; only the
   post-A3 gold Jaccard settles that. (B.1's A2 watch-pair prediction was *falsified* by its §7.2 test —
   the decoupling↔contraception merge did not happen — so treat this read as a hypothesis, not a result.)
2. Term cores are the discriminative centers of each family; broadening them shifts individual cells but
   not the block structure.
3. The recency of the literature means much of the corpus is post-2018 and preprint-heavy; the search
   must not down-weight recent or non-DOI grey-literature sources, or it will miss the phenomenon by
   construction. The five semantic families are worth naming in the query log for vocabulary coverage
   even if the operational budget count collapses to three.
