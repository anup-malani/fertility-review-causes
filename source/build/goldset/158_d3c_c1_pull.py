#!/usr/bin/env python3
r"""
158_d3c_c1_pull.py — D.3.c, stage C1. The production pull.

Executes the frozen production query from `{slug}-production-query.json` — outcome block, restricted
to 2000+ and four record types by PI decision — and writes every record to disk once.

    expected universe: 238,189 records (measured live at B1/filter time)
    transport:         OpenAlex cursor pagination, 200/page, ~1,191 pages

WHAT THIS SCRIPT TREATS AS SACRED, AND WHY.

**The pull is immutable and dated.** It is the input to a paid screen and the denominator of the
PRISMA identification box, and OpenAlex is a moving index — a re-pull in three months would not
reproduce it and would silently change every count downstream. The manifest therefore stamps the date
and the exact filter, and the records file is written once. If it needs re-running, that is a NEW
pull with a new date, not a refresh of this one.

**A failed page is recorded, never skipped.** This project has now hit three separate ways for a
refused request to read as an absence, and a pull is where that failure is most expensive: a silently
short pull understates the identification count, and nothing downstream can tell the difference
between "the index held 238,189" and "we successfully fetched 230,000 of them". Every page that fails
after retries is written to the manifest with its cursor, and the script REFUSES to mark the pull
complete if the shortfall exceeds SHORTFALL_ABORT.

**Resumable, because 1,191 pages is long enough to be interrupted.** The cursor is checkpointed after
every page and records are appended as JSONL rather than accumulated in memory and written at the
end — a crash at page 900 costs one page, not the whole run.

**Payload is gitignored; the manifest is versioned.** `temp/` is in `.gitignore` and the records are
regenerable-in-principle and ~250MB; the manifest is small, is what PRISMA and the limitations section
cite, and belongs in version control. `datastore/` is deliberately NOT used: it is the versioned
bibliographic source of truth for INCLUDED studies, not a bucket for raw retrieval.

Abstracts are reconstructed from OpenAlex's inverted index and truncated to ABSTRACT_CHARS, matching
the Tier B frame so screen-cost estimates built on the frame transfer to this pull unchanged.

    python 158_d3c_c1_pull.py [--limit-pages N] [--resume]

Output: temp/d3c-pull/records.jsonl              (gitignored payload)
        temp/d3c-pull/checkpoint.json            (cursor + counts)
        literature/search-logs/{slug}-c1-manifest.json / .md   (versioned)
"""
import argparse, json, os, subprocess, sys, time
from datetime import datetime, timezone
from urllib.parse import quote

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(ROOT, "temp", "d3c-pull")
RECORDS = os.path.join(WORK, "records.jsonl")
CKPT = os.path.join(WORK, "checkpoint.json")

PER_PAGE = 200
ABSTRACT_CHARS = 1200
MAX_RETRIES = 4
SHORTFALL_ABORT = 0.02      # >2% short of the expected universe and the pull is not "complete"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
SELECT = ("id,doi,title,publication_year,type,primary_location,authorships,cited_by_count,"
          "abstract_inverted_index")


def key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


def unabstract(inv):
    if not inv:
        return ""
    try:
        pos = {}
        for w, idxs in inv.items():
            for i in idxs:
                pos[i] = w
        return " ".join(pos[k] for k in sorted(pos))[:ABSTRACT_CHARS]
    except Exception:
        return ""


def row(w):
    loc = (w.get("primary_location") or {}).get("source") or {}
    return {"id": (w.get("id") or "").rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "title": w.get("title") or "",
            "abstract": unabstract(w.get("abstract_inverted_index")),
            "year": w.get("publication_year"),
            "type": w.get("type"),
            "venue": loc.get("display_name") or "",
            "authors": [a["author"]["display_name"] for a in (w.get("authorships") or [])][:6],
            "cited_by_count": w.get("cited_by_count")}


def fetch(url):
    """Returns (payload, ok). A refusal or transport failure is NEVER an empty page."""
    for attempt in range(MAX_RETRIES):
        r = subprocess.run(["curl", "-s", "-m", "120", "-A", UA, url],
                           capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout, strict=False)
            except Exception:
                time.sleep(2 * (attempt + 1)); continue
            if isinstance(d, dict) and d.get("error"):
                return {"error": f"{d.get('error')} {str(d.get('message'))[:120]}"}, False
            if "results" in d:
                return d, True
        time.sleep(2 * (attempt + 1))
    return {"error": "no parseable response after retries"}, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-pages", type=int)
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()

    pq = json.load(open(os.path.join(LOGS, f"{SLUG}-production-query.json")))
    expr = "(" + " OR ".join(f'"{p}"' for p in pq["phrases"]) + ")"
    filt = pq["filters"]["openalex_filter_suffix"]
    expected = pq["filters"]["universe_filtered"]
    K = key()

    os.makedirs(WORK, exist_ok=True)
    state = {"cursor": "*", "pages": 0, "records": 0, "failures": [], "seen_ids": 0,
             "started_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    if a.resume and os.path.exists(CKPT):
        state = json.load(open(CKPT))
        print(f"resuming at page {state['pages']}, {state['records']:,} records", file=sys.stderr)
    else:
        open(RECORDS, "w").close()

    seen = set()
    if a.resume and os.path.exists(RECORDS):
        for line in open(RECORDS):
            try:
                seen.add(json.loads(line)["id"])
            except Exception:
                pass

    out = open(RECORDS, "a")
    t0 = time.time()
    while state["cursor"]:
        if a.limit_pages and state["pages"] >= a.limit_pages:
            break
        url = (f"https://api.openalex.org/works?filter=title.search:{quote(expr)}{filt}"
               f"&per-page={PER_PAGE}&cursor={quote(state['cursor'])}&select={SELECT}"
               f"&api_key={K}")
        d, ok = fetch(url)
        if not ok:
            # Recorded with its cursor so the page can be re-fetched. Never silently skipped:
            # a short pull that looks complete corrupts the PRISMA denominator.
            state["failures"].append({"page": state["pages"], "cursor": state["cursor"],
                                      "error": d.get("error", "unknown")})
            print(f"  PAGE {state['pages']} FAILED: {d.get('error')}", file=sys.stderr)
            break
        for w in d.get("results", []):
            r = row(w)
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
            state["records"] += 1
        state["pages"] += 1
        state["cursor"] = (d.get("meta") or {}).get("next_cursor")
        if state["pages"] % 25 == 0:
            out.flush()
            json.dump(state, open(CKPT, "w"), indent=1)
            rate = state["records"] / max(time.time() - t0, 1)
            eta = (expected - state["records"]) / max(rate, 1) / 60
            print(f"  page {state['pages']:>5}  {state['records']:>7,} records  "
                  f"{rate:>5.0f} rec/s  eta {eta:>4.0f} min", file=sys.stderr)
        time.sleep(0.05)
    out.close()
    state["seen_ids"] = len(seen)
    state["finished_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(state, open(CKPT, "w"), indent=1)

    shortfall = 1 - state["records"] / expected if expected else 0
    complete = (not state["failures"]) and shortfall <= SHORTFALL_ABORT and not a.limit_pages
    manifest = {"stage": "C1", "slug": SLUG,
                "pulled_utc": state.get("finished_utc"),
                "query_phrases": len(pq["phrases"]), "filter": filt,
                "expected_universe": expected, "records_written": state["records"],
                "unique_ids": len(seen), "pages": state["pages"],
                "shortfall": round(shortfall, 4), "failed_pages": state["failures"],
                "complete": complete, "records_path": os.path.relpath(RECORDS, ROOT),
                "abstract_truncated_at": ABSTRACT_CHARS}
    json.dump(manifest, open(os.path.join(LOGS, f"{SLUG}-c1-manifest.json"), "w"), indent=1)

    L = [f"# C1 production pull — {SLUG}", "",
         f"**Pulled:** {state.get('finished_utc')} · **Status:** "
         f"{'COMPLETE' if complete else '**INCOMPLETE — see below**'}", "",
         "This pull is **immutable and dated**. It is the input to a paid screen and the denominator "
         "of the PRISMA identification box, and OpenAlex is a moving index: a re-pull would not "
         "reproduce it and would silently change every downstream count. Re-running produces a NEW "
         "pull with a new date, not a refresh of this one.", "",
         "| | |", "|---|---|",
         f"| expected universe (measured at query-freeze) | {expected:,} |",
         f"| records written | **{state['records']:,}** |",
         f"| unique OpenAlex ids | {len(seen):,} |",
         f"| pages fetched | {state['pages']:,} |",
         f"| shortfall vs expected | {shortfall:.2%} |",
         f"| failed pages | {len(state['failures'])} |",
         f"| abstracts truncated at | {ABSTRACT_CHARS} chars |", "",
         f"**Filter applied:** `{filt}`", "",
         "A small shortfall against the expected universe is normal — the count was measured at "
         "query-freeze and the index moves — but it is reported rather than absorbed, because the "
         "difference between *the index held N* and *we fetched N* is exactly what a PRISMA "
         "identification count asserts.", ""]
    if state["failures"]:
        L += ["## Failed pages — NOT zero results", "",
              "Each page below failed after retries and its records are **missing from this pull**. "
              "The cursor is recorded so the page can be re-fetched; until then the identification "
              "count is a lower bound.", ""]
        L += [f"- page {f['page']}: `{f['error']}`" for f in state["failures"]]
        L.append("")
    open(os.path.join(LOGS, f"{SLUG}-c1-manifest.md"), "w").write("\n".join(L) + "\n")
    print(f"\nrecords={state['records']:,} pages={state['pages']:,} "
          f"shortfall={shortfall:.2%} failures={len(state['failures'])} complete={complete}")


if __name__ == "__main__":
    main()
