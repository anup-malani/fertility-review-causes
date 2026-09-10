# C.3.f screening rubric — title/abstract

**Frozen 2026-09-10.** Derived from `wealth-flows-reversal-search-scope.md` §2, §8, §9, §10. Batches
are emitted blinded by `source/build/goldset/385_c3f_screen_batches.py`: no provenance, no channel,
no anchor or decoy flag. **Every row gets a verdict, including the obvious excludes** — hidden
controls need a verdict on every row or sensitivity has no denominator.

## The one question that decides most rows

**Which way do the resources move, and is the estimate about the NET of the two?**

C.3.f's registered exposure is the *net* direction of private transfers between parents and their
children — downward (what parents give) minus upward (what children give) — and the claim is that the
net arrow reverses. Net is a difference, so its two components carry **opposite signs by
construction**. A record measuring only one component is evidence on one half of that difference and
is never pooled with the other half or with the net.

Read the estimate, not the framing sentence. A paper may open on Caldwell and then estimate something
else; C.3.d's D.1.b neighbour found four of eight papers doing exactly that.

## Cells

| cell | what it is | role |
|---|---|---|
| `NET_FLOW_FERTILITY` | an exogenous move in the net direction or magnitude of private transfers → realized fertility | **primary** |
| `SHOCK_NET_FERTILITY` | a policy or labour-demand shock → realized fertility, with the flow measured or argued | **primary** |
| `UPWARD_COMPONENT` | upward flow alone (child labour contribution, support to parents, remittances to parents) → fertility | link evidence; never pooled with net |
| `DOWNWARD_COMPONENT` | downward flow or child cost alone → fertility | link evidence; mostly C.2.b's |
| `FLOW_MEASUREMENT` | measures the flow itself, **no fertility outcome** — village studies, NTA profiles | **link 1.** Never primary, never a demsig numerator |
| `VOC_STATED` | an elicited valuation of children → intentions or desires | separate outcome level; never pooled with realized |
| `MIXED_PUBLIC_PRIVATE` | a public transfer substituting for the private flow — pensions, social security, long-term-care insurance | **C.3.c's, a closed chapter.** Route out with a note |
| `MIXED_FLOW_PRODUCTION` | the flow moves because the production system changed | jointly claimed with C.3.a, unallocated |
| `MIXED_FLOW_INCOME` | the flow and household income move together | jointly claimed with C.1.a, unallocated |
| `FLOW_ASSOCIATION` | a flow series against a fertility series, no identified variation | context; never primary |
| `REVERSE` | fertility → the flow, or → expectations of support | context |
| `THEORY` | Caldwell's statements, extensions, critiques; no empirical fertility estimate | context |
| `OFF_SIBLING` | a determinant that is another registry entry's estimand — C.3.d's return to child human capital, D.1.b's cultural diffusion, A.3's ideational diffusion, D.2.a's female autonomy, A.1's mortality. Name the sibling in `note` | route out, named |
| `OFF_TOPIC` | none of the above | out |
| `INSUFFICIENT_INFO` | cannot be routed on the visible record | pairs only with `UNCERTAIN` |

**`OFF_SIBLING` was added mid-probe, in stratum 1, and the earlier strata are unaffected because it was the first.** Without it, Dyson and Moore on kinship and female autonomy, Coale and Watkins on the European decline, and Becker-Murphy-Tamura on the return to human capital would all have been `OFF_TOPIC` — which is true of this chapter and useless to the review, since each is a sibling chapter's central evidence. `add-a-cell-when-the-rubric-lacks-one`.

`add-a-cell-when-the-rubric-lacks-one`: if a real class of record fits nowhere, add a cell and re-run
completed strata rather than forcing it into `OFF_TOPIC`.

## Fields on every row

| field | values |
|---|---|
| `screen_id` | as emitted |
| `cell` | one of the above |
| `flow_direction` | `UPWARD` · `DOWNWARD` · `NET` · `BOTH_MEASURED` · `NA` |
| `flow_object` | `PRIVATE_FAMILY` · `PUBLIC_TRANSFER` · `MIXED` · `NA` |
| `outcome_object` | `FERTILITY` · `FLOW_MAGNITUDE` · `NONE` |
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` · `STATED_VALUATION` · `NA` |
| `identified` | `YES` · `NO` · `UNCLEAR` — a named design (IV, DiD, RDD, RCT, event study, natural experiment) |
| `phenomenon` | `PM` · `FDT` · `SDT` · `OTHER` · `UNCLEAR` |
| `confidence` | `CERTAIN` · `UNCERTAIN` |
| `note` | one line, only where the routing is not obvious |

Screen-stage judgements are **hypotheses, not properties**: every included record is re-read at full
text, and a design named here is re-checked there.

## Routing rules that decide the hard cases

1. **Pensions and social insurance are C.3.c's**, even when framed on Caldwell. A public transfer
   that substitutes for support from children is `MIXED_PUBLIC_PRIVATE`, routed out. C.3.c is closed;
   we inherit its verdict rather than re-run its evidence.
2. **No fertility outcome is not off-topic** if the record measures the flow. That is
   `FLOW_MEASUREMENT`, and §5's demographic-significance route needs it.
3. **Remittances** are in scope only where the estimate is signed on the *transfer* rather than on
   household income; otherwise `MIXED_FLOW_INCOME`, tagged for C.1.a.
4. **Child-labour demand** shocks: if the paper's operative variable is what children produce and the
   outcome is fertility, it is `SHOCK_NET_FERTILITY` with a C.3.a flag. If the outcome is schooling
   or child labour itself, it is `FLOW_MEASUREMENT` or link-1, not primary.
5. **A stated valuation is not a realized flow.** The Value-of-Children survey tradition is
   `VOC_STATED` whatever its outcome.
6. **Non-human fertility** (soil, livestock, crops) is `OFF_TOPIC`. "Fertility" is an agronomy word
   and this universe carries agricultural vocabulary from the §7 rows.
7. When the abstract is absent, judge the title and set `confidence=UNCERTAIN`. 20% of this universe
   is title-only.
