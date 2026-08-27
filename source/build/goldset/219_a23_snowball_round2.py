#!/usr/bin/env python3
"""
219 — A.23 citation snowball, round 2.

TICK-075. Round 1 (217) produced a 2,584-record pool and two measured results that
determine what round 2 does:

  * The pre-launch cloud contained NOT ONE record with both an exposure and a
    fertility term in its title. The citation channel will not, on its own, connect
    that arm to births — so round 2 adds pre-launch seeds chosen because they
    already span the two axes, rather than adding more of the same.
  * The decoy cloud ran 0.6% on-topic against 1.9% elsewhere, because two of the
    four decoys mark a HOMONYM rather than a boundary. No new seeds are spent
    there, and the round-1 decoy records stay in the pool, tagged.

Round 2 therefore does three things:
  1. Pages the forward tails of the two CAPPED pre-launch seeds (Furstenberg 2010,
     Leaving Home in Europe). The Reher and filial-responsibility tails are left
     alone deliberately — they are decoy tails.
  2. Adds 8 pre-launch seeds from the C.2.c harvest, each gated through Crossref
     before it is used.
  3. Merges into the round-1 pool, keeping first_found_round so the two rounds stay
     separable, and re-scores the pre-launch cloud to see whether the round-1
     asymmetry was a property of the seeds or of the literature.

Usage: python3 source/build/goldset/219_a23_snowball_round2.py
"""
import json
import re
import subprocess
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
POOL = LOGS / "co-residence-parents-household-delay-snowball-pool.json"
OUT_LOG = LOGS / "co-residence-parents-household-delay-snowball-round2.json"
API = "https://api.openalex.org/works"
CROSSREF = "https://api.crossref.org/works/"
SELECT = ("id,doi,title,publication_year,type,cited_by_count,primary_location,"
          "authorships,referenced_works")
PER_PAGE = 200

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}

# Round-1 seeds that hit the forward cap AND sit on the pre-launch side.
# The two decoy tails (Reher 1359, filial responsibility 202) are NOT paged.
TAILS_TO_PAGE = [
    ("10.1353/foc.0.0038", "W2119664404_placeholder", 469, "Furstenberg 2010"),
    ("10.1002/ijpg.231", "W_placeholder", 253, "Leaving Home in Europe"),
]

# New pre-launch seeds, chosen because they already span exposure AND fertility --
# the axis pairing the round-1 pre-launch cloud never produced.
NEW_SEEDS = [
    ("10.1553/populationyearbook2008s57", "Institutions and the transition to adulthood: implications for fertility tempo", "PRIMARY_PRELAUNCH"),
    ("10.4054/demres.2017.36.20", "The timing of marriage vis-a-vis coresidence and childbearing", "PRIMARY_PRELAUNCH"),
    ("10.1016/j.alcr.2014.08.001", "Moving and union formation in the transition to adulthood in the United States", "LINK1_ARRANGEMENT_TO_UNION"),
    ("10.20377/jfr-953", "Employment conditions and non-coresidential partnership in very-low fertility countries", "PRIMARY_PRELAUNCH"),
    ("10.1080/13229400.2025.2452243", "Family migration in Chinese superstar cities: fertility intentions of migrants", "PRIMARY_PRELAUNCH"),
    ("10.1080/13676261.2015.1112884", "Parental co-residence, shared living and emerging adulthood in Europe", "PRIMARY_PRELAUNCH"),
    ("10.1007/s13524-013-0247-8", "Gender, Turning Points, and Boomerangs: Returning Home in Young Adulthood", "PRIMARY_PRELAUNCH"),
    ("10.1006/juec.1998.2083", "Prices, Parents, and Young People's Household Formation", "LINK1_DRIVER_TO_ARRANGEMENT"),
]

PRELAUNCH_RE = re.compile(
    r"co-?resid|living with (?:their )?parents?|liv\w* at home|parental (?:home|nest)|"
    r"leav\w* (?:the )?(?:parental |family )?(?:home|nest)|home-?leaving|nest-?leav|"
    r"boomerang|residential (?:independence|autonomy)|household formation|"
    r"transition to adulthood|young adults?", re.I)
FERT_RE = re.compile(
    r"fertilit|childbear|child-?bearing|first birth|second birth|birth rate|"
    r"parenthood|childless|family size|number of children|tfr\b", re.I)


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def fold(s):
    if not s:
        return ""
    s = s.lower()
    s = "".join(TRANSLIT.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def get(params, tries=3):
    args = ["curl", "-sS", "--max-time", "150", "--get", API]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    last = None
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            last = f"curl-{r.returncode}"
            time.sleep(5 * (attempt + 1)); continue
        try:
            d = json.loads(r.stdout)
        except Exception:
            last = "parse"; time.sleep(5 * (attempt + 1)); continue
        if "error" in d:
            last = str(d["error"])[:60]; time.sleep(10 * (attempt + 1)); continue
        return d, None
    return None, last


def crossref_ok(doi):
    """Existence gate. Returns (ok, resolved_title, error)."""
    url = CROSSREF + doi
    for attempt in range(3):
        r = subprocess.run(["curl", "-sS", "--max-time", "60", "-H",
                            "User-Agent: fertility-review (mailto:shravanh@uchicago.edu)", url],
                           capture_output=True, text=True)
        if r.returncode != 0:
            time.sleep(4 * (attempt + 1)); continue
        if r.stdout.strip().startswith("Resource not found"):
            return False, None, "NOT_IN_CROSSREF"
        try:
            m = json.loads(r.stdout)["message"]
            return True, (m.get("title") or [None])[0], None
        except Exception:
            time.sleep(4 * (attempt + 1))
    return False, None, "ERROR"


def shape(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    return {
        "openalex": w["id"].rsplit("/", 1)[-1],
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "title": w.get("title"), "norm_title": fold(w.get("title")),
        "year": w.get("publication_year"), "type": w.get("type"),
        "venue": src.get("display_name"), "cited_by": w.get("cited_by_count"),
        "authors": "; ".join(a["author"]["display_name"]
                             for a in (w.get("authorships") or [])[:4]),
    }


def main():
    pool = {r["openalex"]: r for r in json.loads(POOL.read_text())}
    before = len(pool)
    errors, gate = {}, []

    def absorb(w, seed_doi, direction, round_no=2):
        rec = pool.get(w["id"].rsplit("/", 1)[-1])
        if rec is None:
            rec = shape(w)
            rec.update({"seeds_backward": [], "seeds_forward": [],
                        "first_found_round": round_no, "n_seeds": 0, "no_doi_flag": rec["doi"] is None})
            pool[rec["openalex"]] = rec
        key = "seeds_backward" if direction == "back" else "seeds_forward"
        if seed_doi not in rec[key]:
            rec[key].append(seed_doi)
        return rec

    # --- 1. gate the new seeds ----------------------------------------------
    print("gating 8 new pre-launch seeds through Crossref")
    good_seeds = []
    for doi, label, cell in NEW_SEEDS:
        ok, resolved, err = crossref_ok(doi)
        gate.append({"doi": doi, "recorded": label, "resolved_title": resolved,
                     "existence": "FOUND" if ok else ("ERROR" if err == "ERROR" else "UNRESOLVED"),
                     "cell": cell})
        print(f"  {'FOUND     ' if ok else 'UNRESOLVED'} {doi:36s} {(resolved or '')[:52]}")
        if ok:
            good_seeds.append((doi, cell))

    # --- 2. resolve seeds to OpenAlex and snowball ---------------------------
    print(f"\nsnowballing {len(good_seeds)} gated seeds")
    seed_ids = []
    for doi, cell in good_seeds:
        d, err = get([("filter", f"doi:{doi}"), ("per-page", "1"), ("select", SELECT)])
        if err or not d.get("results"):
            errors[f"resolve:{doi}"] = err or "no_openalex_record"
            print(f"  no OpenAlex record: {doi}")
            continue
        w = d["results"][0]
        seed_ids.append((doi, w["id"].rsplit("/", 1)[-1], cell))
        refs = [r.rsplit("/", 1)[-1] for r in (w.get("referenced_works") or [])]
        for i in range(0, len(refs), 50):
            dd, e = get([("filter", "openalex_id:" + "|".join(refs[i:i + 50])),
                         ("per-page", "50"), ("select", SELECT)])
            if e:
                errors[f"back:{doi}:{i}"] = e; continue
            for ww in dd.get("results", []):
                absorb(ww, doi, "back")
        dd, e = get([("filter", f"cites:{w['id'].rsplit('/', 1)[-1]}"),
                     ("per-page", str(PER_PAGE)), ("sort", "cited_by_count:desc"),
                     ("select", SELECT)])
        if e:
            errors[f"fwd:{doi}"] = e
        else:
            for ww in dd.get("results", []):
                absorb(ww, doi, "fwd")
            print(f"  {len(refs):3d} refs, {dd['meta']['count']:4d} citations  {doi}")

    # --- 3. page the two capped pre-launch tails -----------------------------
    print("\npaging the two capped PRE-LAUNCH forward tails (decoy tails left alone)")
    tail_added = {}
    for doi, _, total, label in TAILS_TO_PAGE:
        d, err = get([("filter", f"doi:{doi}"), ("per-page", "1"), ("select", "id")])
        if err or not d.get("results"):
            errors[f"tail-resolve:{doi}"] = err or "no_record"; continue
        wid = d["results"][0]["id"].rsplit("/", 1)[-1]
        n0 = len(pool)
        for page in (2, 3):
            dd, e = get([("filter", f"cites:{wid}"), ("per-page", str(PER_PAGE)),
                         ("page", str(page)), ("sort", "cited_by_count:desc"),
                         ("select", SELECT)])
            if e:
                errors[f"tail:{doi}:p{page}"] = e; break
            got = dd.get("results", [])
            for ww in got:
                absorb(ww, doi, "fwd")
            if len(got) < PER_PAGE:
                break
        tail_added[doi] = len(pool) - n0
        print(f"  +{tail_added[doi]:4d} new records from the tail of {label} ({total} citations)")

    # --- 4. re-score, keeping the rounds separable ---------------------------
    records = list(pool.values())
    for r in records:
        r["n_seeds"] = len(r["seeds_backward"]) + len(r["seeds_forward"])
        r.setdefault("no_doi_flag", r["doi"] is None)
    records.sort(key=lambda r: (-r["n_seeds"], -(r["cited_by"] or 0)))

    new_seed_dois = {d for d, _ in good_seeds}
    # NOTE: `&` binds tighter than `|`, so writing this as
    #   set(back) | set(fwd) & new_seed_dois
    # is `set(back) | (set(fwd) & new_seed_dois)` -- truthy whenever the record has ANY
    # backward seed, which scored 2,010 records as the round-2 pre-launch cloud on the
    # first run. Parenthesise the union.
    prelaunch_cloud = [r for r in records
                       if (set(r["seeds_backward"]) | set(r["seeds_forward"])) & new_seed_dois]
    both = sum(1 for r in prelaunch_cloud
               if PRELAUNCH_RE.search(r["title"] or "") and FERT_RE.search(r["title"] or ""))
    fert = sum(1 for r in prelaunch_cloud if FERT_RE.search(r["title"] or ""))
    n = len(prelaunch_cloud) or 1

    log = {
        "meta": {
            "ticket": "TICK-075", "round": 2,
            "pool_before": before, "pool_after": len(records),
            "added": len(records) - before,
            "new_seeds_gated": len(gate),
            "new_seeds_found": len(good_seeds),
            "tail_pages_added": tail_added,
            "errors": len(errors),
            "round2_prelaunch_cloud": {
                "n": len(prelaunch_cloud),
                "fertility_outcome_pct": round(100 * fert / n, 1),
                "both_axes_pct": round(100 * both / n, 1),
                "round1_comparison": "round-1 pre-launch cloud was n=219, 11.4% fertility, 0.0% both axes",
            },
            "not_paged_deliberately": [
                "10.2307/2807972 (Reher 1998, 1359 citations) — theory/Wall-3 decoy tail",
                "10.2307/353569 (filial responsibility, 202 citations) — elder-support decoy tail",
            ],
        },
        "existence_gate": gate,
        "errors": errors,
    }
    POOL.write_text(json.dumps(records, indent=1))
    OUT_LOG.write_text(json.dumps(log, indent=1))
    print("\n" + json.dumps(log["meta"], indent=1))


if __name__ == "__main__":
    main()
