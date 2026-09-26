#!/usr/bin/env python3
"""
93_d1d_make_screen_batches.py — D.1.d (nationalist and pronatalist ideology), stage-3 screen input.

Prepare the merged ~2,867-record screen frame (92) for blinded title/abstract LLM screening. No record is
filtered here (keep-and-route): pruning by vocabulary distance would bias recall. Records are
deterministically shuffled, stripped of discovery provenance (source_channels, cited_by_count, doi are
blinded), and split into fixed-size batches. A committed manifest records paths + SHA-256; batch payloads
live in temp/ (reproducible from the committed frame).

Mirror of 93_d2c. SLUG, SEED, and the rubric (D.1.d's cells, its SIX walls, its FDT/SDT scope, the two
MIXED bundled-treatment cells, and the load-bearing REVERSE cell) differ. The routing decoys must surface
route-away: Milligan 2005 -> OFF_TRANSFERS; Pop-Eleches 2006 -> OFF_ABORTION_BAN; Lesthaeghe-Surkyn 1988 ->
OFF_SECULARIZATION; Frejka-Westoff 2008 -> OFF_RELIGIOSITY; La Ferrara 2012 -> OFF_DIFFUSION_CHANNEL;
Nugent 1985 -> OFF_OLD_AGE_SECURITY.

Inputs : literature/search-logs/{slug}-screen-frame.json
Outputs: temp/screen/{slug}/batch_NNN.json, RUBRIC.md
         literature/search-logs/{slug}-screen-manifest.json
         literature/search-logs/{slug}-screen-rubric.md
"""
import hashlib, json, random
from pathlib import Path

SLUG = "nationalism-pronatalist-ideology"
SEED = 931  # D.1.d / TICK-093
BATCH_SIZE = 40
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)

RUBRIC = """# Blinded title/abstract screening rubric — nationalist and pronatalist ideology (D.1.d) — v1

## Review question

Does the paper bear on **D.1.d** — the claim that **state-sponsored nationalist and pronatalist IDEOLOGY**
(the normative framing of childbearing as a patriotic or national duty, propagated through propaganda,
rhetoric, and honorific awards for large families) **raises fertility**, with modest and mostly transient
effects? D.1.d's parameter is the effect of the **ideological framing itself** on realized fertility —
**holding fixed the financial transfers and the coercive fertility-control restrictions that almost always
accompany it** — and whether that effect is a durable quantum shift or a transient tempo response.

Judge ONLY the supplied title and abstract. Discovery channel and citation count are intentionally hidden.
Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states the
estimand verbatim (e.g. "Pronatalist propaganda and the birth rate"); route such a record normally but set
`identification` to `NA` unless the title also names the design. In every other abstract-less case use
`UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a substantive cell for a record you know
nothing about — that corrupts the cell counts.

**Phenomenon scope is FDT and SDT (NOT PM).** Organized nationalist-pronatalist ideology is a modern-state
phenomenon: interwar/mid-century authoritarian natalism (Fascist Italy's Battle for Births, Nazi/Vichy/
Soviet natalism) in the FDT, and contemporary "demographic nationalism" (Hungary, Russia, Turkey, Iran,
Israel) in the SDT. A pre-modern or purely traditional-norm fertility study is OUT of scope for this
chapter (route to a cultural sibling or NOT_RELEVANT).

## THE SIX LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs C.2.d (Tax and Transfer Pronatalism). LOAD-BEARING.** Pronatalist regimes bundle propaganda
with money (child allowances, baby bonuses, parental leave, childcare, tax credits). D.1.d owns the
FRAMING; C.2.d owns the CASH. A study identifying off a financial transfer/benefit/tax incentive is
`OFF_TRANSFERS`. A study identifying off propaganda/rhetoric/patriotic framing with transfers held fixed
stays here (a PRIMARY cell). A study of a pronatalist package where ideology and money CANNOT be separated
is `MIXED_IDEOLOGY_TRANSFER` (still RELEVANT — it is an upper bound on the ideational channel).

**Wall 2 — vs A.4/A.2 (Abortion / Contraception). LOAD-BEARING.** The most-cited "pronatalist" natural
experiments (Romania's Decree 770, 1966) raised fertility by BANNING abortion/contraception — coercion,
not persuasion. A study identifying off restriction/removal of abortion or contraception ACCESS is
`OFF_ABORTION_BAN`. A study identifying off ideological framing that leaves the means of fertility control
untouched stays here. A study of an episode that combines a ban with propaganda inseparably is
`MIXED_IDEOLOGY_COERCION` (still RELEVANT — an upper bound).

**Wall 3 — vs D.1.a (Postmaterialism / Individualism / Secularization).** D.1.a owns the diffuse, bottom-up
secular/individualist value shift that LOWERS fertility. D.1.d owns the deliberate, top-down, state-
sponsored nationalist framing that RAISES it (opposite-signed, different agent). A study identifying off
secularization/individualism/post-materialist value change is `OFF_SECULARIZATION`. A study identifying off
a nationalist-pronatalist campaign stays here.

**Wall 4 — vs religiosity (the D.1.a secularization arm).** Diffuse personal/denominational religiosity ->
fertility routes to `OFF_RELIGIOSITY`. A study identifying off the STATE's instrumentalization of religious-
national identity for an explicit demographic-national goal stays here. Diffuse faith is not D.1.d.

**Wall 5 — vs A.20 (Cultural Diffusion Mechanisms).** A.20 owns the CHANNEL through which any norm spreads
(mass media, social networks, radio/TV) regardless of message content. D.1.d owns the pronatalist-
nationalist MESSAGE. A study whose object is the media/network channel regardless of the message is
`OFF_DIFFUSION_CHANNEL`. A study whose object is the pronatalist-nationalist message's effect on fertility
stays here (and may cite A.20 as the vehicle).

**Wall 6 — vs C.3.c (Old-Age Security).** One economic ROOT/motive for pronatalism is old-age support. A
study identifying off pensions/formal old-age support is `OFF_OLD_AGE_SECURITY`. A study identifying off
ideological framing stays here.

## Estimand cells

- `PRIMARY_CAMPAIGN_EXPOSURE`: exposure to a pronatalist propaganda/ideology campaign (by region, media
  reach, cohort), transfers and abortion law held fixed -> births / fertility. The cleanest ideational
  identification.
- `PRIMARY_RHETORIC_INTENSITY`: cross-national/temporal variation in nationalist-pronatalist ideology
  intensity, net of the financial package -> TFR / completed fertility.
- `PRIMARY_PATRIOTIC_FRAMING_MICRO`: individual national identification / patriotic-duty framing (incl.
  framing/priming experiments), economics held fixed -> fertility intentions / behaviour.
- `MIXED_IDEOLOGY_TRANSFER`: a pronatalist campaign bundled inseparably with transfers -> fertility.
  RELEVANT; an upper bound on the ideational channel. Cross-ref C.2.d.
- `MIXED_IDEOLOGY_COERCION`: a pronatalist campaign bundled inseparably with an abortion/contraception
  restriction -> fertility. RELEVANT; an upper bound. Cross-ref A.4/A.2.
- `MECHANISM_IDEOLOGY_ONLY`: documents pronatalist ideology/rhetoric levels or trends with NO fertility
  outcome. Mechanism/context.
- `THEORY`: formal/theoretical model of ideology and fertility with no own empirical estimate.
- `OFF_TRANSFERS`: identification off a financial transfer/benefit/tax incentive. Route to C.2.d (Wall 1).
- `OFF_ABORTION_BAN`: identification off restriction/removal of abortion or contraception access. Route to
  A.4/A.2 (Wall 2).
- `OFF_SECULARIZATION`: identification off secularization / individualism / post-materialist value shift.
  Route to D.1.a (Wall 3).
- `OFF_RELIGIOSITY`: identification off personal/denominational religiosity. Route to D.1.a relig (Wall 4).
- `OFF_DIFFUSION_CHANNEL`: identification off the media/network channel regardless of message. Route to
  A.20 (Wall 5).
- `OFF_OUTCOME`: nationalism/pronatalism -> a NON-fertility outcome (voting, migration attitudes, national
  sentiment, war mobilisation). Mechanism / context only.
- `OFF_OTHER`: a non-D.1.d determinant of fertility with no sibling-hypothesis home above.
- `REVERSE`: fertility/demographic DECLINE -> the rise of nationalist-pronatalist politics or the state's
  ADOPTION of pronatalism. The direction is backwards; takes `NOT_RELEVANT` unless it ALSO carries an
  ideology -> fertility estimand. A load-bearing confound in this literature.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a pronatalist-ideology exposure (a campaign, rhetoric-intensity variation, or patriotic-duty
   framing) AND a fertility / birth / intention outcome must be present for a PRIMARY or MIXED cell.
2. **The identification tags.** Set `identification=NATURAL_EXPERIMENT` when the design uses an exogenous
   shock — differential propaganda exposure, a regime/campaign change, a discontinuity — to isolate the
   ideational channel. Set `identification=FRAMING_EXPERIMENT` for a survey/priming/vignette experiment on
   patriotic-duty or national-identity framing. A cross-section correlating stated national identity /
   rhetoric intensity with fertility, or a raw before/after comparison confounded with policy, is
   `ASSOCIATIONAL_ONLY`. Such a paper is still `RELEVANT` if it bears on the estimand; the tag records that
   it is not cleanly identified. Never upgrade an association to an identified effect.
3. **The bundling rule (Wall 1/Wall 2).** The historical norm is that ideology travels with money and often
   with coercion. If the design isolates the ideology, use a PRIMARY cell. If it cannot separate ideology
   from transfers, use `MIXED_IDEOLOGY_TRANSFER`; from an abortion/contraception ban, `MIXED_IDEOLOGY_
   COERCION`. Do NOT silently credit a bundled effect to ideology.
4. **The reverse-causality rule.** Demographic decline is a powerful CAUSE of pronatalist politics. A paper
   whose object is why a state ADOPTED pronatalism, or that pronatalist regimes have low fertility, is
   `REVERSE` and usually `NOT_RELEVANT` — it has the arrow backwards. Only a design with exogenous
   variation in EXPOSURE to the ideology identifies the forward effect.
5. Do not promote an OFF-cell paper to PRIMARY merely because it mentions nationalism or population.
   Conversely, do not demote a genuine ideology -> fertility estimand merely because it also reports policy
   or economic covariates (that is what MIXED cells are for).
6. Reviews and syntheses of the core estimand MAY take a PRIMARY cell. Set `evidence_type=review`; the
   assembler excludes reviews from the pooled estimate.
7. **Homonyms are `NOT_RELEVANT` / `NA`.** "national fertility (rate)" meaning a country's TFR (not
   nationalism), "population policy" as a family-planning catch-all, "nationality"/"nationals" =
   citizenship, "nationalization" of industry, and "natal" in medicine (pre-/post-/neo-/ante-natal care)
   are out of scope unless the paper is genuinely about pronatalist IDEOLOGY and fertility. Say which
   homonym in `reason`.
8. Contentless records — prefaces, front matter, tables of contents, editorial notes — are `NOT_RELEVANT` /
   `NA`, not `UNCERTAIN`.
9. `sub_mechanism` is descriptive, not a router: `PROPAGANDA_CAMPAIGN`, `PATRIOTIC_FRAMING`,
   `RHETORIC_INTENSITY`, `HONORIFIC_AWARDS`, or `NA`.
10. `evidence_type` is a short design label, not a router. Two tokens are load-bearing and MUST be used
    verbatim because they drive downstream pooling exclusion: exactly `review` for ANY review/meta-analysis,
    and exactly `theory` for ANY purely theoretical/formal-model paper with no own estimate. Else give the
    closest of `quasi-experimental`, `observational`, `structural`, `qualitative`, `descriptive`,
    `mechanism`, or `other`.

## Output

Return ONLY a JSON array, one object per input record, IN THE SAME ORDER, each with exactly:
`id`, `verdict` (RELEVANT|UNCERTAIN|NOT_RELEVANT), `estimand_cell`, `sub_mechanism`, `outcome` (short
phrase for the fertility outcome, or "none"), `identification`
(NATURAL_EXPERIMENT|FRAMING_EXPERIMENT|ASSOCIATIONAL_ONLY|UNCLEAR|NA), `evidence_type`, `reason` (one
sentence).
"""


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = LOGS / f"{SLUG}-screen-frame.json"
    records = json.loads(source.read_text())
    ids = [r.get("id") for r in records]
    if any(not v for v in ids) or len(ids) != len(set(ids)):
        raise SystemExit("frame must have unique, nonblank id values")

    shuffled = list(records)
    random.Random(SEED).shuffle(shuffled)
    (SCREEN / "RUBRIC.md").write_text(RUBRIC)
    manifest, assigned = [], []
    for start in range(0, len(shuffled), BATCH_SIZE):
        number = start // BATCH_SIZE + 1
        batch = []
        for row in shuffled[start:start + BATCH_SIZE]:
            batch.append({
                "id": row["id"],
                "title": row.get("title") or "",
                "year": row.get("year"),
                "abstract": (row.get("abstract") or "")[:3500],
            })
            assigned.append(row["id"])
        ip = SCREEN / f"batch_{number:03d}.json"
        ip.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
        manifest.append({"batch": number, "n": len(batch),
                         "input": str(ip.relative_to(REPO)), "input_sha256": sha256(ip),
                         "output": str((SCREEN / f"verdict_{number:03d}.json").relative_to(REPO))})
    if len(assigned) != len(records) or set(assigned) != set(ids):
        raise SystemExit("batch coverage invariant failed")

    committed = {"slug": SLUG, "stage": "blinded_title_abstract_screen_input",
                 "source": str(source.relative_to(REPO)), "source_sha256": sha256(source),
                 "seed": SEED, "batch_size": BATCH_SIZE, "n_records": len(records),
                 "n_batches": len(manifest), "manifest": manifest}
    (LOGS / f"{SLUG}-screen-manifest.json").write_text(json.dumps(committed, indent=2))
    (LOGS / f"{SLUG}-screen-rubric.md").write_text(RUBRIC)
    print(f"records {len(records)}, batches {len(manifest)} (size {BATCH_SIZE}, seed {SEED})")
    print(f"wrote manifest and rubric to {LOGS}")
    print(f"batch payloads in {SCREEN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
