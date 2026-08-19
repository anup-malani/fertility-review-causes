#!/usr/bin/env python3
r"""
157_d3c_lower_recall_options.py — D.3.c. Price the lower-recall pull options.

The full pull is 390,983 records and its two-stage screen costs ~$134 (155_), against a documented
project expectation of ~$37 per hypothesis (`decisions/2026-06-20-llm-screening-pipeline.md`). This
script prices the ways of buying that number down, so the trade is a table rather than an argument.

Each option is measured, not assumed:
  * **Pull size** — live OpenAlex counts against the frozen production query.
  * **Gold cost** — computed locally against the 243 gold records that carry an id in the frame,
    using each record's own year and type. This is the same gold B1 used.
  * **Dollars** — the 155_ cost model re-run at the reduced volume.

WHAT THIS SCRIPT CANNOT TELL YOU, AND SAYS SO IN ITS OUTPUT. A percentage recall loss is a poor guide
when the target cell is small. The open-database ceiling on this chapter's actual claim is **65
records** (mechanism AND treatment AND a fertility outcome, measured 2026-08-18), and the primary cell
is some subset of those. Losing "8% of gold" is a statement about a 243-record proxy; against a
65-record ceiling the same filter might remove five of the studies the chapter rests on, or none. The
variance matters more than the mean at that scale, and no filter here is chosen on the mean.

Output: literature/search-logs/{slug}-lower-recall-options.md
"""
import json, os, statistics, subprocess, sys, urllib.parse

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")

TYPES_BROAD = {"article", "review", "book-chapter", "report", "preprint", "dissertation", "book"}
TYPES_MID = {"article", "review", "book-chapter", "report"}

OPTIONS = [
    ("baseline — full recall",            None, None,        ""),
    ("year >= 1990",                      1990, None,        ",from_publication_date:1990-01-01"),
    ("year >= 2000",                      2000, None,        ",from_publication_date:2000-01-01"),
    ("type: broad (7 types)",             None, TYPES_BROAD, ",type:article|review|book-chapter|report|preprint|dissertation|book"),
    ("type: mid (4 types)",               None, TYPES_MID,   ",type:article|review|book-chapter|report"),
    ("1990 + broad types",                1990, TYPES_BROAD, ",from_publication_date:1990-01-01,type:article|review|book-chapter|report|preprint|dissertation|book"),
    ("1990 + mid types",                  1990, TYPES_MID,   ",from_publication_date:1990-01-01,type:article|review|book-chapter|report"),
    ("2000 + mid types",                  2000, TYPES_MID,   ",from_publication_date:2000-01-01,type:article|review|book-chapter|report"),
]

# Cost model constants, kept identical to 155_ so the two agree by construction.
CHARS_PER_TOKEN, RECORDS_PER_REQUEST = 4.0, 20
S1_RUBRIC, S1_OUT, S2_RUBRIC, S2_OUT = 1_500, 40, 3_000, 200
S1_PASS, BATCH, CACHE_READ = 0.15, 0.50, 0.10
P_HAIKU, P_SONNET = {"in": 1.00, "out": 5.00}, {"in": 2.00, "out": 10.00}
D1_KEEP = 0.92     # 154_: D1 removes only 8% at lossless gold recall


def key():
    for line in open(os.path.join(ROOT, ".env")):
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


def live_count(expr, extra, k):
    url = (f"https://api.openalex.org/works?filter=title.search:{urllib.parse.quote(expr)}{extra}"
           f"&per-page=1&select=id&api_key={k}")
    out = subprocess.run(["curl", "-s", "-m", "90", "-A", "ua", url],
                         capture_output=True, text=True).stdout
    try:
        d = json.loads(out, strict=False)
        return d["meta"]["count"] if "meta" in d else None
    except Exception:
        return None


def stage(n, chars, rubric, out_per, price):
    reqs = max(1, round(n / RECORDS_PER_REQUEST))
    rec_tok = n * chars / CHARS_PER_TOKEN
    eff_in = rec_tok + reqs * rubric * CACHE_READ
    return ((eff_in / 1e6) * price["in"] + (n * out_per / 1e6) * price["out"]) * (1 - BATCH)


def total_cost(pull, chars):
    n1 = pull * D1_KEEP
    return stage(n1, chars, S1_RUBRIC, S1_OUT, P_HAIKU) + \
           stage(n1 * S1_PASS, chars, S2_RUBRIC, S2_OUT, P_SONNET)


def main():
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location("cvb", os.path.join(HERE, "152_d3c_cv_breadth.py"))
    cvb = importlib.util.module_from_spec(spec); sys.modules["cvb"] = cvb
    spec.loader.exec_module(cvb)
    gold, _n, _nc, _nn, _a = cvb.load()
    tb = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))
    byk = {cvb.norm(r.get("title") or "")[:70]: r for r in tb if r.get("title")}
    g = [byk[cvb.norm(x["title"])[:70]] for x in gold if cvb.norm(x["title"])[:70] in byk]
    chars = statistics.mean(len((r.get("title") or "") + " " + (r.get("abstract") or "")) for r in tb)

    pq = json.load(open(os.path.join(LOGS, f"{SLUG}-production-query.json")))
    expr = "(" + " OR ".join(f'"{p}"' for p in pq["phrases"]) + ")"
    k = key()

    rows = []
    for label, yr, types, extra in OPTIONS:
        kept = [r for r in g
                if (yr is None or (r.get("year") or 0) >= yr)
                and (types is None or r.get("type") in types)]
        lost = len(g) - len(kept)
        pull = live_count(expr, extra, k)
        rows.append(dict(label=label, pull=pull, gold_kept=len(kept), gold_lost=lost,
                         recall=len(kept) / len(g),
                         cost=total_cost(pull, chars) if pull else None))
        print(f"  {label:<26} pull={format(pull,',') if pull else 'ERR':>9}  "
              f"gold={len(kept)}/{len(g)} ({len(kept)/len(g):.1%})  "
              f"${rows[-1]['cost']:.0f}" if pull else f"  {label}: ERROR")

    base = rows[0]
    L = [f"# D.3.c — lower-recall pull options, priced", "",
         "The full pull is **390,983** records and its screen costs **~$134** (155_), against the "
         "project's documented **~$37 per hypothesis** "
         "(`decisions/2026-06-20-llm-screening-pipeline.md`). This table prices the ways of buying "
         "that down. Pull sizes are **live counts**; gold costs are computed against the 243 gold "
         "records carrying an id, using each record's own year and type; dollars re-run 155_'s model "
         "at the reduced volume.", "",
         "| option | pull | vs base | gold recall | gold lost | screen cost | saving |",
         "|---|---|---|---|---|---|---|"]
    for r in rows:
        if not r["pull"]:
            continue
        L.append(f"| {r['label']} | {r['pull']:,} | {r['pull']/base['pull']-1:+.0%} | "
                 f"{r['recall']:.1%} | {r['gold_lost']} | ${r['cost']:.0f} | "
                 f"${base['cost']-r['cost']:.0f} |")
    best = min((r for r in rows[1:] if r["pull"]), key=lambda r: r["cost"])
    L += ["", "## What the table says", "",
          f"**The most aggressive option measured — {best['label']} — saves "
          f"${base['cost']-best['cost']:.0f} and costs {best['gold_lost']} of {len(g)} gold records "
          f"({1-best['recall']:.1%}).** Every option is a poor trade, and the reason is that the "
          "levers available are orthogonal to what makes this corpus big.", "",
          "A date floor and a type filter both cut *volume*, and volume is cheap: the screen is $134 "
          "for 390,983 records, so a 39% volume cut saves about $50. What they cost is *recall*, and "
          "recall is the only thing in this chapter that cannot be bought back later. The exchange "
          "rate is bad in both directions at once.", "",
          "## The percentage is the wrong unit", "",
          "**A recall loss expressed as a percentage is a poor guide when the target cell is small.** "
          "The open-database ceiling on this chapter's actual claim — a fertility outcome, a despair "
          "construct and an economic treatment together — is **65 records**, and the primary cell is "
          "some subset of those. \"8% of gold\" is a statement about a 243-record provenance proxy; "
          "against a 65-record ceiling the same filter might remove five of the studies the chapter "
          "rests on, or none. At that scale the variance matters more than the mean, and none of "
          "these filters is chosen on the mean.", "",
          "The date floor is also **not neutral between the two chapters**. B1 measured which records "
          "a 1990 floor drops: Duncan and Hoffman (1990) on welfare, economic opportunity and "
          "out-of-wedlock births, and the early-1990s teen-childbearing literature — chapter 2's "
          "canon, not chapter 1's. The deaths-of-despair framing is recent; the acceleration "
          "mechanism's evidence is not. A date floor is a chapter-1 convenience paid for by "
          "chapter 2, and the PI's Call 1 ruling made chapter 2 a first-class deliverable rather "
          "than an appendix.", "",
          "## Recommendation", "",
          f"**Run the full pull at ${base['cost']:.0f}.** If the ~$37 line is a hard ceiling rather "
          "than a planning figure, the honest fix is to amend the line — it assumes a "
          "conjunction-narrowed corpus of 50K-100K records, which is exactly what this chapter could "
          "not have — not to buy the number down with recall this chapter cannot spare.", "",
          "If a reduction is required anyway, **`type: broad (7 types)` is the least-bad option**: it "
          "drops `paratext`, `editorial`, `letter`, `erratum` and similar non-research records, which "
          "are things the screen would reject regardless. It is the only filter here that removes "
          "records for a reason connected to whether they could be evidence.", ""]
    open(os.path.join(LOGS, f"{SLUG}-lower-recall-options.md"), "w").write("\n".join(L) + "\n")
    print(f"\n-> literature/search-logs/{SLUG}-lower-recall-options.md")


if __name__ == "__main__":
    main()
