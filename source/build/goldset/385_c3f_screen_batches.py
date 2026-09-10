#!/usr/bin/env python3
"""385 — hydrate the C.3.f universe with abstracts, then emit blinded screening batches.

Port of C.3.d's 354 (itself C.2.f's 341, C.2.b's 322), with two changes this chapter forced.

**Hydration.** 384 built the universe from counts and ids and did not keep abstracts. They are
fetched here by id, 200 at a time, and cached — a title-only screen is a much weaker screen and on
this chapter the routing calls turn on the DIRECTION of a transfer, which titles rarely state.

**Ordering.** C.3.d's universe arrived citation-ranked, so an evenly spaced probe walked the yield
curve by construction. This one arrives arm by arm, so it is sorted by citation count before
striding. Without that the "strata" would be arms wearing a probe's clothes.

Everything else is inherited because it was paid for elsewhere:

* `--probe K N` takes N records from each of K evenly spaced strata. Screening front-to-back tells
  you the yield of the head and nothing about the tail (`citation-sorted-head-is-not-the-population`,
  `probe-depth-dont-screen-sequentially`). On C.3.d stratum 1 held ZERO primary records.
* Batches are **BLINDED**: no provenance, no channel, no anchor or decoy flag. The channel predicts
  the cell — a record from the SHOCK arm is a policy design, one from FLOW_MEASUREMENT has no
  fertility outcome by construction — so showing it would make the screen agree with the query
  instead of reading the record (`blinded-screen-audits-the-anchors`).
* **Every emitted row comes back with a verdict**, including the obvious excludes, or sensitivity
  has no denominator (`a-positives-only-screen-cannot-measure-sensitivity`).
* `title_only` is carried per row, because a title-only judgement must be visible as one.
* ABSTRACT_CHARS is **1800, not 460**. TICK-085 was opened because a 460-character cap hid the
  dependent variable on 35.8% of C.3.d's universe. Do not lower it for token cost: the cap buys a
  saving by hiding the field the direction ruling turns on.

Usage:
  385 --hydrate                 fetch and cache abstracts for the whole universe
  385 --probe 8 25              8 evenly spaced strata x 25 records
  385 --channel FLOWMEAS 60     one channel exhaustively, mixed with size-matched decoys
  385 --remaining 60            everything with no verdict yet, in batches of 60
"""
import argparse, csv, json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "source" / "lib"))
from openalex import OpenAlex                                      # noqa: E402

UNIVERSE = ROOT / "output" / "wealth-flows-reversal-universe.json"
HYDRATED = ROOT / "temp" / "c3f-universe-hydrated.json"
OUT = ROOT / "extraction" / "wealth-flows-reversal-screen-batches"
VERDICTS = ROOT / "extraction" / "wealth-flows-reversal-screen-verdicts.csv"
ABSTRACT_CHARS = 1800
KEEP = ("screen_id", "title", "year", "venue", "type", "cited_by", "abstract", "title_only")


def abstract_of(rec):
    inv = rec.get("abstract_inverted_index")
    if not inv:
        return ""
    return " ".join(w for _, w in sorted((p, w) for w, ps in inv.items() for p in ps))


def hydrate():
    recs = json.loads(UNIVERSE.read_text())["records"]
    key = ""
    for line in open(ROOT / ".env"):
        if line.startswith("OPENALEX_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"')
    oa = OpenAlex(key=key, mailto="shravanh@uchicago.edu",
                  cache_path=str(ROOT / "temp" / "c3f-hydrate-cache.json"))
    have = {}
    if HYDRATED.exists():
        have = {r["id"]: r for r in json.loads(HYDRATED.read_text())["records"]}
    todo = [r["id"] for r in recs if r["id"] not in have or have[r["id"]].get("abstract") is None]
    # ids.openalex caps at 100 VALUES per filter, whatever per-page allows. The first attempt sent
    # 200 and was refused with "Maximum number of values exceeded".
    CHUNK = 100
    print(f"{len(have)} already hydrated, {len(todo)} to fetch "
          f"({-(-len(todo) // CHUNK)} requests)")
    for i in range(0, len(todo), CHUNK):
        chunk = todo[i:i + CHUNK]
        d, err = oa.get({"filter": "ids.openalex:" + "|".join(chunk), "per-page": "200",
                         "select": "id,display_name,publication_year,type,cited_by_count,"
                                   "abstract_inverted_index,primary_location"})
        if err:
            # A refusal is not an empty abstract — and the first version of this function proved
            # the point on itself: it printed the refusal, broke out, and then WROTE THE FILE
            # anyway, reporting 4,565 records as title-only. That artifact would have gone into a
            # screen as a fact about the literature. `a-partial-run-must-write-nothing`: a run that
            # could not buy what it needed writes nothing and exits non-zero.
            sys.exit(f"REFUSED at chunk {i // CHUNK} ({len(have)} hydrated before the refusal). "
                     f"Nothing written. {err}")
        for r in d.get("results", []):
            pid = r["id"].rsplit("/", 1)[-1]
            loc = r.get("primary_location") or {}
            src = (loc.get("source") or {}).get("display_name")
            have[pid] = {"id": pid, "title": r.get("display_name"),
                         "year": r.get("publication_year"), "type": r.get("type"),
                         "cited_by": r.get("cited_by_count"), "venue": src,
                         "abstract": abstract_of(r)}
        if (i // CHUNK) % 10 == 0 or i + CHUNK >= len(todo):
            print(f"  hydrated {min(i + CHUNK, len(todo))}/{len(todo)}", flush=True)
    prov = {r["id"]: r.get("provenance", []) for r in recs}
    out = []
    for r in recs:
        h = have.get(r["id"], {})
        out.append({"id": r["id"], "title": h.get("title") or r.get("title"),
                    "year": h.get("year") or r.get("year"), "type": h.get("type") or r.get("type"),
                    "cited_by": h.get("cited_by", r.get("cited_by")), "venue": h.get("venue"),
                    "abstract": h.get("abstract", ""), "provenance": prov[r["id"]]})
    HYDRATED.parent.mkdir(exist_ok=True)
    HYDRATED.write_text(json.dumps({"n": len(out), "records": out}, indent=1) + "\n")
    n_abs = sum(1 for r in out if (r.get("abstract") or "").strip())
    print(f"\nhydrated {len(out)} records; {n_abs} have an abstract "
          f"({100 * n_abs / len(out):.0f}%), {len(out) - n_abs} are title-only")
    if n_abs < 0.3 * len(out):
        sys.exit(f"only {n_abs} of {len(out)} records came back with an abstract. 382 measured 23 "
                 "of 24 anchors as having one, so this is a broken run and not a title-only "
                 "literature. File written but treat it as suspect.")


def load():
    if not HYDRATED.exists():
        sys.exit("run --hydrate first: a title-only screen of this universe is not the screen")
    recs = json.loads(HYDRATED.read_text())["records"]
    # Citation-sorted, so an evenly spaced probe strides the yield curve rather than the arms.
    recs.sort(key=lambda r: -(r.get("cited_by") or 0))
    # Ids are FROZEN by 387 and read from the file, never recomputed. They were position-based, so
    # any change to the universe -- 387 removed 384 records -- would otherwise renumber everything
    # below the first removal and silently invalidate every verdict already written
    # (`stage-output-must-survive-rerun`).
    missing = [r for r in recs if not r.get("screen_id")]
    if missing:
        sys.exit(f"{len(missing)} records carry no frozen screen_id. Run 387 to freeze them before "
                 "emitting batches; recomputing them here would renumber the universe.")
    for r in recs:
        r["title_only"] = not (r.get("abstract") or "").strip()
    return recs


def emit(rows, name):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(
        {"name": name, "n": len(rows), "records": rows}, indent=1) + "\n")
    L = [f"# Screen batch `{name}` — {len(rows)} records", "",
         "Blinded: no provenance, no channel, no anchor or decoy flag. Apply",
         "`literature/search-logs/wealth-flows-reversal-screen-rubric.md`. **Every row needs a",
         "verdict**, including the obvious excludes.", ""]
    for i, r in enumerate(rows, 1):
        ab = (r.get("abstract") or "").strip()
        ab = (ab[:ABSTRACT_CHARS] + "…") if len(ab) > ABSTRACT_CHARS else (ab or "**NO ABSTRACT**")
        L += [f"### {i}. `{r['screen_id']}` — {r.get('title') or '(untitled)'}",
              f"*{r.get('year') or '?'} · {r.get('venue') or 'no venue'} · "
              f"{r.get('type') or '?'} · cited "
              f"{r.get('cited_by') if r.get('cited_by') is not None else '?'}*", "", ab, ""]
    (OUT / f"{name}.md").write_text("\n".join(L))
    print(f"wrote {name}: {len(rows)} records")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hydrate", action="store_true")
    ap.add_argument("--probe", nargs=2, type=int, metavar=("STRATA", "PER"))
    ap.add_argument("--channel", nargs=2, metavar=("NAME", "SIZE"),
                    help="screen one provenance channel exhaustively, mixed with size-matched "
                         "decoys from the rest and shuffled, so the channel is not inferable from "
                         "a row's position")
    ap.add_argument("--remaining", type=int, metavar="SIZE")
    ap.add_argument("--decoy-ratio", type=float, default=0.5)
    a = ap.parse_args()

    if a.hydrate:
        return hydrate()

    recs = load()
    slim = [{k: r.get(k) for k in KEEP} for r in recs]

    if a.channel:
        name, size = a.channel[0], int(a.channel[1])
        by_id = {r["screen_id"]: r for r in recs}
        tgt = [r["screen_id"] for r in recs
               if any(p.startswith(name) for p in r.get("provenance") or [])]
        rest = [r["screen_id"] for r in recs
                if not any(p.startswith(name) for p in r.get("provenance") or [])]
        random.seed(86)
        decoys = random.sample(rest, min(len(rest), int(len(tgt) * a.decoy_ratio)))
        ids = tgt + decoys
        random.shuffle(ids)
        rows = [{k: by_id[i].get(k) for k in KEEP} for i in ids]
        for j in range(0, len(rows), size):
            emit(rows[j:j + size], f"chan-{name.lower()}-{j // size:02d}")
        print(f"\n{len(tgt)} in {name} (exhaustive) + {len(decoys)} decoys = {len(ids)} rows, "
              f"shuffled. Channel membership is NOT in the emitted rows.")
    elif a.probe:
        k, per = a.probe
        span = len(slim) / k
        for s in range(k):
            lo = int(s * span)
            emit(slim[lo:lo + per], f"probe-s{s + 1}-of-{k}")
        print(f"\n{k} strata x {per} = {k * per} of {len(slim)} records "
              f"({100 * k * per / len(slim):.0f}%), evenly spaced by citation rank")
    elif a.remaining:
        done = set()
        if VERDICTS.exists():
            with VERDICTS.open() as f:
                done = {r["screen_id"] for r in csv.DictReader(f)}
        left = [r for r in slim if r["screen_id"] not in done]
        print(f"{len(done)} already screened, {len(left)} remaining of {len(slim)}")
        for i in range(0, len(left), a.remaining):
            emit(left[i:i + a.remaining], f"rest-{i // a.remaining:03d}")
    else:
        ap.error("give --hydrate, --probe, --channel or --remaining")


main()
