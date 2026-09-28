#!/usr/bin/env python3
"""
93_a20_make_screen_batches.py — A.20 (cultural diffusion mechanisms), stage-3 screen input.

Prepare the merged ~5,095-record screen frame (92) for blinded title/abstract LLM screening. No record is
filtered here (keep-and-route): pruning by vocabulary distance would bias recall. Records are
deterministically shuffled, stripped of discovery provenance (source_channels, cited_by_count, doi are
blinded), and split into fixed-size batches. A committed manifest records paths + SHA-256; batch payloads
live in temp/ (reproducible from the committed frame).

Mirror of 93_d1d, INVERTED. A.20 owns the diffusion CHANNEL (media reach, network position, community
boundary) regardless of content; the SIX walls route the CONTENT/CAUSE away. The routing decoys must
surface route-away: Cleland-Wilson 1987 -> OFF_CONTENT_FERTILITY_CONTROL (A.3); Fernandez-Fogli 2009 ->
OFF_VERTICAL (A.19); Goldin-Katz 2002 -> OFF_TECHNOLOGY (A.2); Miller 2010 -> OFF_PROGRAM_CONTENT (A.5);
Lesthaeghe-Surkyn 1988 -> OFF_CONTENT_VALUE_SHIFT (D.1.a); King 1998 -> OFF_CONTENT_VALUE_SHIFT (D.1.d).
The empirical core must surface PRIMARY: La Ferrara 2012 / Jensen-Oster 2009 -> PRIMARY_MEDIA_CHANNEL;
Kohler-Behrman-Watkins 2001 -> PRIMARY_NETWORK_PEER.

Inputs : literature/search-logs/{slug}-screen-frame.json
Outputs: temp/screen/{slug}/batch_NNN.json, RUBRIC.md
         literature/search-logs/{slug}-screen-manifest.json
         literature/search-logs/{slug}-screen-rubric.md
"""
import hashlib, json, random
from pathlib import Path

SLUG = "cultural-diffusion-mechanisms"
SEED = 941  # A.20 / TICK-094
BATCH_SIZE = 40
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)

RUBRIC = """# Blinded title/abstract screening rubric — cultural diffusion mechanisms (A.20) — v1

## Review question

Does the paper bear on **A.20** — the claim that the **CHANNELS through which norms and information spread**
(social-network architecture, mass-media reach — radio, TV, soap operas — and linguistic/cultural community
boundaries) **shape the pace and geography of fertility change, independent of the CONTENT of the norm and
the REASON desired fertility changed**? A.20's parameter is the effect of the **channel itself** on
fertility (or on the speed/spatial pattern of its change) — the conduit, not the message. It explains why a
transition happened here-before-there or fast-rather-than-slow, not why desired fertility fell.

Judge ONLY the supplied title and abstract. Discovery channel and citation count are intentionally hidden.
Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states the
estimand verbatim (e.g. "Cable television and fertility in India"); route such a record normally but set
`identification` to `NA` unless the title also names the design. In every other abstract-less case use
`UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a substantive cell for a record you know
nothing about — that corrupts the cell counts.

**Phenomenon scope is FDT and SDT (NOT PM).** A.20 is a mechanism of spread: it presupposes a norm or
innovation that propagates. The FDT stream is the Princeton European Fertility Project signature (decline
clustering by language/religion, crossing borders on a timetable development does not reproduce). The SDT
stream is the mass-media and social-network evidence. A pre-modern standing-equilibrium fertility study is
OUT of scope for this chapter.

## THE KEY AXIS: CHANNEL vs CONTENT/CAUSE

A.20 is a mechanism/channel hypothesis, so it overlaps every CONTENT hypothesis that diffuses. On EVERY
wall the discriminator is the same: **does the study's identification come from the CHANNEL (A.20) or from
the CONTENT / the cause of changed demand (a neighbour)?** A media/network/boundary study whose treatment
is content-agnostic REACH or STRUCTURE stays here; a study whose object is the specific message, the
device, or why demand fell routes away.

## THE SIX LOAD-BEARING BOUNDARY WALLS (frozen, hard lines)

**Wall 1 — vs A.3 (Diffusion and Social-Learning of Fertility CONTROL). LOAD-BEARING.** A.3 owns the
diffused CONTENT — the knowledge and legitimacy of deliberately limiting births. A.20 owns the CHANNEL that
content rides on. A study whose object is the spread of fertility-control knowledge/legitimacy specifically
is `OFF_CONTENT_FERTILITY_CONTROL`. A study whose object is the media/network channel regardless of the
message — above all a mass-media REACH study or an entertainment-media rollout (novela, cable TV) — stays
here (a PRIMARY cell). The precedent: the Brazil telenovela and India cable-TV quasi-experiments are A.20,
because their treatment is signal coverage of general entertainment, not a family-planning message. A study
that cannot separate channel from content (a media campaign that both reached people AND carried an explicit
family-planning message) is `MIXED_CHANNEL_CONTENT` (still RELEVANT — an upper bound on the channel effect).

**Wall 2 — vs A.19 (Intergenerational Transmission).** A.19 owns VERTICAL (parent-to-child) transmission of
family-size preferences. A.20 owns HORIZONTAL spread across peers, media audiences, and community members.
A study identifying off parent-child correlation or ancestral-culture persistence (the epidemiological /
immigrant design) is `OFF_VERTICAL`. A study identifying off a horizontal channel stays here.

**Wall 3 — vs A.2 (Contraceptive Technology).** A.2 is the spread of the physical METHOD (the Pill, the IUD)
and access to it. A.20 is the spread of NORMS/information through channels (historically on withdrawal and
abstinence, no device). A technology-access or method-availability design is `OFF_TECHNOLOGY`. A channel
study carrying norms rather than devices stays here.

**Wall 4 — vs A.5 (Family-Planning Programs).** A.5 is exogenous program SUPPLY, including deliberate IEC /
mass-media family-planning campaigns with a message. A.20 is the content-agnostic channel. A study
identifying off a program's deliberate family-planning campaign (message-specific) is `OFF_PROGRAM_CONTENT`.
A study identifying off content-agnostic media REACH (does having TV/radio/cable at all move fertility,
whatever the programming) stays here. A program's diffusion SPILLOVER to untreated neighbours through social
contact stays here (PRIMARY_NETWORK_PEER) where the object is the channel of spillover.

**Wall 5 — vs D.1 (the value shift / content: D.1.a secularization, D.1.d nationalism).** D.1 owns WHAT
norm is spreading and WHY desired fertility changed (secular/individualist drift -> D.1.a; state
nationalist framing -> D.1.d). A.20 owns HOW any such norm spreads. A study whose object is the message's
effect on fertility (secularization -> fertility; nationalist framing -> fertility) is
`OFF_CONTENT_VALUE_SHIFT`. A study whose object is the channel regardless of the message stays here (and may
cite D.1 as the content it carried).

**Wall 6 — identified diffusion vs descriptive clustering (the reflection problem).** Spatial, linguistic,
or network CLUSTERING of fertility decline is consistent with channel-driven diffusion but equally with the
clustering of the decline's own economic/cultural causes (a common shock hitting connected people together
— Manski's correlated effects) or with homophily in network formation. A study that establishes clustering
WITHOUT exogenous variation in the channel has NOT identified A.20's parameter, however tight the
correlation. Such a study is `MECHANISM_CHANNEL_DESCRIPTIVE` (RELEVANT — it belongs in the descriptive
residual, not the pooled estimate), with `identification=ASSOCIATIONAL_ONLY`. Only designs with exogenous
channel variation (staggered media rollout, signal-geography discontinuities, plausibly-exogenous network
position) are PRIMARY.

## Estimand cells

- `PRIMARY_MEDIA_CHANNEL`: content-agnostic media REACH / signal coverage / entertainment-media rollout
  (TV, radio, cable, novela), message NOT a deliberate family-planning instruction -> fertility /
  contraceptive adoption / pace of change. The cleanest channel identification.
- `PRIMARY_NETWORK_PEER`: social-network position / peer behaviour / network density, content held fixed
  (incl. program diffusion spillover through social contact) -> fertility / contraceptive adoption.
- `PRIMARY_LINGUISTIC_BOUNDARY`: linguistic/religious/cultural community boundary as conduit and barrier
  (the Princeton signature), net of fundamentals -> marital fertility / timing & geography of decline.
- `MECHANISM_CHANNEL_DESCRIPTIVE`: clustering/correlation of decline by space, language, or network WITHOUT
  exogenous channel variation -> fertility. RELEVANT; descriptive residual, not pooled (reflection problem
  unresolved).
- `MIXED_CHANNEL_CONTENT`: channel bundled inseparably with a specific message (a family-planning media
  campaign that both reached AND instructed) -> fertility. RELEVANT; an upper bound on the channel effect.
  Cross-ref A.3 / A.5.
- `THEORY`: formal/theoretical model of diffusion/social interaction and fertility with no own empirical
  estimate.
- `OFF_CONTENT_FERTILITY_CONTROL`: object is the spread of fertility-control knowledge/legitimacy
  specifically. Route to A.3 (Wall 1).
- `OFF_VERTICAL`: object is parent-to-child transmission / ancestral-culture persistence. Route to A.19
  (Wall 2).
- `OFF_TECHNOLOGY`: object is the spread of / access to physical contraceptive methods. Route to A.2
  (Wall 3).
- `OFF_PROGRAM_CONTENT`: object is a deliberate family-planning program message (IEC campaign content).
  Route to A.5 (Wall 4).
- `OFF_CONTENT_VALUE_SHIFT`: object is the message's effect — secularization/individualism -> fertility, or
  nationalist framing -> fertility. Route to D.1.a / D.1.d (Wall 5).
- `OFF_OUTCOME`: media/network -> a NON-fertility outcome (voting, consumption, health, attitudes).
  Mechanism / context only.
- `OFF_OTHER`: a non-A.20 determinant of fertility with no sibling-hypothesis home above.
- `REVERSE`: fertility/demographic change -> media adoption or network formation. The direction is
  backwards; takes `NOT_RELEVANT` unless it ALSO carries a channel -> fertility estimand.
- `INSUFFICIENT_INFO`: cannot be routed on the visible record. Pairs ONLY with `UNCERTAIN`.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. Both a diffusion-CHANNEL exposure (media reach, network position/structure, or a community boundary) AND
   a fertility / birth / contraceptive-adoption / pace-of-change outcome must be present for a PRIMARY,
   MIXED, or MECHANISM cell.
2. **The identification tags.** Set `identification=NATURAL_EXPERIMENT` when the design uses exogenous
   channel variation — a staggered media rollout, signal-geography discontinuity, cable-introduction
   timing. Set `identification=NETWORK_DESIGN` for a plausibly-exogenous or instrumented network/peer
   design that addresses the reflection problem. A cross-section correlating media access / network position
   / linguistic cluster with fertility, or raw spatial clustering, is `ASSOCIATIONAL_ONLY` (-> usually
   MECHANISM_CHANNEL_DESCRIPTIVE). `UNCLEAR` or `NA` otherwise. Never upgrade an association or a clustering
   pattern to an identified channel effect.
3. **The content-vs-channel rule (Wall 1/Wall 4/Wall 5).** A media/network study identifies A.20 only if
   its treatment is content-agnostic (reach/structure). If the channel carried a SPECIFIC message that is
   itself the treatment (a family-planning campaign, a secular/nationalist message), it is an OFF cell or
   MIXED_CHANNEL_CONTENT, not a PRIMARY channel effect. Entertainment media whose small-family portrayal is
   ambient (novela, general cable) is a PRIMARY channel effect.
4. **The reflection-problem rule (Wall 6).** Clustering is not diffusion. A paper that shows fertility
   decline clusters by space/language/network without separating the endogenous social-interaction effect
   from common shocks and homophily is `MECHANISM_CHANNEL_DESCRIPTIVE`, not PRIMARY.
5. Do not promote an OFF-cell paper to PRIMARY merely because it mentions media, networks, or diffusion.
   Conversely, do not demote a genuine channel -> fertility estimand merely because it also reports content
   or economic covariates.
6. Reviews and syntheses of the core estimand MAY take a PRIMARY/MECHANISM cell. Set `evidence_type=review`;
   the assembler excludes reviews from the pooled estimate.
7. **Homonyms are `NOT_RELEVANT` / `NA`.** "diffusion" in physics/chemistry/technology/marketing (diffusion
   coefficient, technology diffusion of a product), "social network ANALYSIS" as a pure method with no
   substantive channel-> fertility claim, generic "media effects" or "communication" on a non-fertility
   outcome, and "network" in an unrelated sense (neural/computer/transport networks) are out of scope
   unless the paper is genuinely about a diffusion channel and fertility. Say which homonym in `reason`.
8. Contentless records — prefaces, front matter, tables of contents, editorial notes — are `NOT_RELEVANT` /
   `NA`, not `UNCERTAIN`.
9. `sub_mechanism` is descriptive, not a router: `MASS_MEDIA`, `SOCIAL_NETWORK`, `PEER_EFFECT`,
   `LINGUISTIC_BOUNDARY`, `SOCIAL_LEARNING`, or `NA`.
10. `evidence_type` is a short design label, not a router. Two tokens are load-bearing and MUST be used
    verbatim because they drive downstream pooling exclusion: exactly `review` for ANY review/meta-analysis,
    and exactly `theory` for ANY purely theoretical/formal-model paper with no own estimate. Else give the
    closest of `quasi-experimental`, `observational`, `structural`, `qualitative`, `descriptive`,
    `mechanism`, or `other`.

## Output

Return ONLY a JSON array, one object per input record, IN THE SAME ORDER, each with exactly:
`id`, `verdict` (RELEVANT|UNCERTAIN|NOT_RELEVANT), `estimand_cell`, `sub_mechanism`, `outcome` (short
phrase for the fertility outcome, or "none"), `identification`
(NATURAL_EXPERIMENT|NETWORK_DESIGN|ASSOCIATIONAL_ONLY|UNCLEAR|NA), `evidence_type`, `reason` (one
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
