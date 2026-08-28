#!/usr/bin/env python3
"""
235_a23_retrieval_handoff.py — A.23, stage 5d. Split what is left into worklists for humans.

After 5b and 5c, 95 of 436 are on disk. This script decides what the remaining 341 are, and the
decision it makes is the A.17 one: **a blocked route is not a paywall.** On A.17, 67 of 98 retrieval
failures were open urls killed by bot defence, and handing all 98 to one person as "paywalled" would
have wasted the effort of the 67 that a browser opens in a second.

So the residue is split by WHAT WOULD FIX IT, not by how it failed:

  W1  BROWSER. The route returned a 200 and served something that was not the article — a bot
      challenge, a splash page, an abstract. The content is open; the door is shut to a script. A
      logged-in browser session opens these. `route_blocked` and `empty_or_tiny` land here.
  W2  LIBRARY / PROXY. No open location on any rung and the record has a DOI. These are genuinely
      closed and need institutional access. A browser will not help without a subscription.
  W3  LIBRARIAN. No DOI at all. No proxy resolves them and no rung can construct a url; they need a
      catalogue search, an interlibrary request, or an author email. Books, chapters, dissertations
      and grey literature concentrate here.

**THE WORKLISTS ARE ORDERED BY TIER AND DESIGN, NOT BY SIZE.** The chapter's retrieval problem is
not its rate, it is its SHAPE: 3 of 26 in the Wall 1 packet and 5 of 22 identified designs, against
19% overall. A worklist sorted by what is easy would put the 193 link-1 records first and leave the
open ruling unread. Each worklist therefore leads with T1 and with identified designs, and each
carries its own cross-tab so whoever works it can stop when the tiers that matter are done.

**THE COUNT THAT DECIDES WHETHER STAGE 5 IS FINISHED IS PRINTED FIRST**, and it is not the overall
rate. It is the Wall 1 packet and the identified designs, because those are what the open ruling and
the GRADE rating rest on.

Output: extraction/{slug}-retrieval-handoff.csv
        literature/search-logs/{slug}-retrieval-handoff.md
"""
import csv, json, os, re
from collections import Counter, defaultdict

SLUG = "co-residence-parents-household-delay"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
FETCH = os.path.join(LOGS, f"{SLUG}-fetch-log.csv")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT_CSV = os.path.join(EXTRACT, f"{SLUG}-retrieval-handoff.csv")
OUT_MD = os.path.join(LOGS, f"{SLUG}-retrieval-handoff.md")

TIER_ORDER = ["T1_wall1_packet", "T1_primary_identified", "T2_primary_relevant",
              "T3_primary_uncertain", "T3_link1_identified",
              "T4_insufficient_resolve_at_retrieval", "T5_link1", "T6_theory_stream"]
DESIGN_RANK = {"identified": 0, "observational": 1, "cannot_tell": 2, "descriptive": 3, "theory": 4}
WORK_NOTE = {
    "W1_browser": "a 200 that was not the article — open content behind bot defence, a splash "
                  "page, or an abstract. A browser session opens these.",
    "W2_library_proxy": "no open location on any rung, but the record has a DOI. Genuinely closed; "
                        "needs institutional access.",
    "W3_librarian": "no DOI at all. No proxy resolves these and no rung can construct a url — a "
                    "catalogue search, an interlibrary request, or an author email.",
}


def on_disk():
    """Everything recovered by ANY stage, including 5c's text files, keyed by OpenAlex id."""
    got = set()
    if not os.path.isdir(PDF_DIR):
        return got
    for f in os.listdir(PDF_DIR):
        m = re.match(r"(W\d+)__", f)
        if m and os.path.getsize(os.path.join(PDF_DIR, f)) > 1024:
            got.add(m.group(1))
    return got


def main():
    meta = {r["id"]: r for r in json.load(open(OA))}
    log = {r["id"]: r for r in csv.DictReader(open(FETCH))}
    have = on_disk()

    rows = []
    for wid, m in meta.items():
        if wid in have:
            continue
        L = log.get(wid, {})
        outcome = L.get("outcome", "no_url")
        if not m.get("doi"):
            work = "W3_librarian"
        elif outcome in ("route_blocked", "empty_or_tiny", "exception"):
            work = "W1_browser"
        else:
            work = "W2_library_proxy"
        rows.append(dict(
            work=work, tier=m["tier"], design=m["design"], route=m["route"],
            verdict=m["verdict"], id=wid, doi=m.get("doi") or "", year=m.get("year") or "",
            venue=m.get("venue") or "", type=m.get("type") or "", is_oa=m["is_oa"],
            outcome=outcome, last_url=L.get("url", "") or m.get("best_url") or "",
            title=(m["title"] or "")[:150]))

    rows.sort(key=lambda r: (r["work"], TIER_ORDER.index(r["tier"]) if r["tier"] in TIER_ORDER else 9,
                             DESIGN_RANK.get(r["design"], 9), r["title"]))
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["work", "tier", "design", "route", "verdict", "id", "doi",
                                           "year", "venue", "type", "is_oa", "outcome", "last_url",
                                           "title"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    tiers = Counter(m["tier"] for m in meta.values())
    have_tier = Counter(m["tier"] for wid, m in meta.items() if wid in have)
    designs = Counter(m["design"] for m in meta.values())
    have_design = Counter(m["design"] for wid, m in meta.items() if wid in have)
    by_work = defaultdict(list)
    for r in rows:
        by_work[r["work"]].append(r)

    crit = [r for r in rows if r["tier"].startswith("T1") or r["design"] == "identified"]
    crit_by_work = Counter(r["work"] for r in crit)

    L = [f"# Stage 5d retrieval handoff — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/235_a23_retrieval_handoff.py`", "",
         f"**{len(have)} of {len(meta)} records are on disk ({pc(len(have), len(meta))})** after the "
         f"scripted fetch and the PMC text recovery. **{len(rows)} are not**, and they are split "
         "below by what would fix them rather than by how they failed.", "",
         "## The number that decides whether stage 5 is finished", "",
         "It is not the overall rate. It is these two rows:", "",
         "| | Wanted | On disk | |", "|---|---|---|---|",
         f"| **Wall 1 packet** | {tiers['T1_wall1_packet']} | {have_tier['T1_wall1_packet']} | "
         f"{pc(have_tier['T1_wall1_packet'], tiers['T1_wall1_packet'])} |",
         f"| **Identified designs** | {designs['identified']} | {have_design['identified']} | "
         f"{pc(have_design['identified'], designs['identified'])} |", "",
         "The Wall 1 packet holds the open ruling on whether this chapter has an identified core at "
         "all, and the identified designs carry whatever GRADE rating each arm gets. A rate computed "
         "over all 436 records answers neither question.", "",
         "## Coverage by tier", "", "| Tier | Wanted | On disk | |", "|---|---|---|---|"]
    for t in TIER_ORDER:
        if tiers.get(t):
            L.append(f"| `{t}` | {tiers[t]} | {have_tier[t]} | {pc(have_tier[t], tiers[t])} |")
    L += ["", "## Coverage by design", "", "| Design | Wanted | On disk | |", "|---|---|---|---|"]
    for d in sorted(designs, key=lambda x: DESIGN_RANK.get(x, 9)):
        L.append(f"| `{d}` | {designs[d]} | {have_design[d]} | {pc(have_design[d], designs[d])} |")
    L += ["", "## The three worklists", "",
          "Split by what would fix each record, because a blocked route and a paywall go to "
          "different people. On A.17, 67 of 98 failures were open urls killed by bot defence; "
          "handing all 98 to one person as \"paywalled\" would have wasted the 67 a browser opens "
          "in a second.", "",
          "| Worklist | n | Of which critical | What it is |", "|---|---|---|---|"]
    for w in ["W1_browser", "W2_library_proxy", "W3_librarian"]:
        L.append(f"| `{w}` | {len(by_work[w])} | {crit_by_work[w]} | {WORK_NOTE[w]} |")
    L += ["", f"**{len(crit)} of the {len(rows)} unretrieved records are critical** — Wall 1 packet "
          "or an identified design. They lead every worklist, because a worklist sorted by what is "
          "easy would put the 193 link-1 records first and leave the open ruling unread.", ""]
    for w in ["W1_browser", "W2_library_proxy", "W3_librarian"]:
        g = [r for r in by_work[w] if r["tier"].startswith("T1") or r["design"] == "identified"]
        if not g:
            continue
        L += [f"### `{w}` — the critical head ({len(g)} of {len(by_work[w])})", "",
              "| Tier | Design | Record | Route to try |", "|---|---|---|---|"]
        for r in g:
            u = r["last_url"] or (f"https://doi.org/{r['doi']}" if r["doi"] else "—")
            L.append(f"| `{r['tier']}` | `{r['design']}` | {r['title'][:78]} | {u[:88]} |")
        L.append("")
    L += ["The full lists, all three worklists and every tier, are in "
          f"`extraction/{SLUG}-retrieval-handoff.csv`.", "",
          "## What this does not claim", "",
          "- **`W2` is closed by our evidence, not by the publisher's.** It means no rung this "
          "pipeline runs found an open copy. A copy on a personal page, in a repository OpenAlex "
          "does not index, or under a title variant is not ruled out.",
          "- **`W1` is a prediction that a browser will work**, and it should be measured like any "
          "other rung — how many of the browser attempts actually delivered — rather than assumed.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"on disk {len(have)}/{len(meta)} ({pc(len(have), len(meta))}); handoff {len(rows)}")
    print("worklists:", {w: len(by_work[w]) for w in by_work})
    print("critical unretrieved:", len(crit), dict(crit_by_work))
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
