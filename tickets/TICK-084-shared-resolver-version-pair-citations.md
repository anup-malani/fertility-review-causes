# TICK-084: Version-pair citation splitting belongs in the shared resolver
**Status:** open
**Assigned:** any
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** `source/lib/` (a new module or an addition to the resolver helpers), `docs/`

## The defect

A single published study can appear in OpenAlex as two or more records that split its citation mass.
Every chapter that anchors on such a work seeds its snowball on whichever record its resolver
happened to rank first, and a low-citation record yields a near-empty citing set that reads as an
absence rather than as a retrieval failure.

**Three distinct shapes have now been observed, and they need different handling.**

1. **A publisher DOI migration, both records live.** Black, Devereux & Salvanes 2005 carries
   `10.1162/0033553053970179` (1,051 cites) *and* `10.1093/qje/120.2.669` (446) — the QJE
   MIT-Press-to-OUP migration. Same title, year, venue and authors, so the title gate, the author
   gate and the year gate all pass on both and none of them discriminates.
2. **A preprint out-citing its version of record.** Rosenzweig & Zhang: the SSRN preprint (2006, 65)
   out-cites the *Review of Economic Studies* version (2009, 11).
3. **A version of record with essentially no recorded citations and no twin to merge.** Galor & Moav
   2002, "Natural Selection and the Origin of Economic Growth": the QJE record
   (`10.1162/003355302320935007`) carries **1** citation and the SSRN preprint 93, for a work cited
   in the thousands. `filter=doi:10.1093/qje/117.4.1133` returns **no record**, so unlike shape 1
   there is nothing to reconcile — OpenAlex's citation graph never attached to the published
   version. Doepke 2004 is the same shape at 11 vs 145.

## Why this is a shared-library ticket and not a per-chapter one

**A.12 said so, on 2026-08-21, in `161_a12_cold_start_anchors.py`:** the QJE migration "will recur in
EVERY chapter that anchors on QJE and is therefore worth its own note rather than a local fix." It
did not get one. It recurred on C.3.d (TICK-083) on 2026-09-09, on the same study — Black, Devereux
& Salvanes is a Tier-A anchor for both chapters — plus two instances of shape 3 that A.12 had not
seen.

There is a memory note, `qje-doi-migration-splits-citations`, saying the same thing. A lesson
recorded and not implemented is a lesson that bites again, which is what happened.

Chapters that anchor on QJE, JPE, Econometrica or ReStud — that is most of the economic ones — are
all exposed. A.12, C.3.d and C.2.f all anchor on Black-Devereux-Salvanes.

## What to build

1. **A version-pair resolver in `source/lib/`.** Given a resolved work, return every index record
   that is the same study: DOI-migration twins, preprint/VOR pairs, and repository deposits of the
   same title. C.3.d's `351_c3d_snowball_seeds.py` is a working sketch of the output shape — union
   the pair, keep every id, report the version-of-record's share — but it only sees twins the
   anchor resolver happened to surface in the same result set, which is a floor rather than a search.
2. **A known-migration table.** The MIT-Press→OUP QJE prefix pair is deterministic and worth
   encoding rather than rediscovering: `10.1162/00335530…` ↔ `10.1093/qje/…`. Shape 3 shows the
   OUP twin does not always exist, so a lookup must tolerate a miss without treating it as an error.
3. **A `dead_version_of_record` flag**, as in `351`: when the version of record holds under ~10% of
   the pair's citations, seeding a snowball on it alone will return near-nothing, and that must be
   loud rather than silent.
4. **A retro-audit.** Every chapter that has already run a snowball did so on some seed set. Report
   which of those seeds were dead versions of record, and how much citing literature was therefore
   never reachable. This is the same shape as the `version-of-record-gate` memory note: OAS, B.1 and
   D.3.b gold was never re-graded after that gate was found.

## Note on scope

`version-pair-is-one-study` makes a preprint twin **one** study at extraction — do not let this
ticket's union-the-pair rule leak into the extraction table, where it would double-count. One study
for extraction, two seeds for retrieval; they are different questions and the library should make
that explicit rather than leaving each chapter to remember it.

## Log
