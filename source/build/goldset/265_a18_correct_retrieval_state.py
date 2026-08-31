#!/usr/bin/env python3
"""265 — A.18: correct the retrieval state against what the text corpus proved. TICK-076.

263 reported 108/148 retrieved (73.0%). That was wrong. 264 converted every
retrieved file to text and found that **46 of them are bot-challenge pages** —
Cloudflare "Client Challenge", "Just a moment... Enable JavaScript and cookies" —
served with HTTP 200 and enough raw markup to clear a byte threshold, but stripping
to between 11 and 303 characters. A further 6 are abstract-only landing pages.

**HTTP 200 plus bytes is not a retrieval.** The only test that works is whether the
text contains a paper. This is `blocked-route-is-not-a-paywall` one layer deeper:
those 46 are not paywalled and not fetched — they are bot-blocked, and they belong
in the browser-job queue, which was 43 records shorter than it should have been.

True position: **56 of 148 full texts (37.8%)**. This script rewrites the state and
regenerates the handoff so no downstream stage inherits the inflated figure.

Usage: python3 source/build/goldset/265_a18_correct_retrieval_state.py
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
STATE = LOGS / "heritability-fertility-genetic-retrieval-state.json"
CORPUS = LOGS / "heritability-fertility-genetic-corpus-log.json"
OUT_MD = LOGS / "heritability-fertility-genetic-retrieval-handoff.md"
PRIORITY = ["PREDICTED_RESPONSE", "H2_MODERATION", "WITHIN_VS_POPULATION",
            "PEDIGREE_RESPONSE", "SELECTION_DIFFERENTIAL", "H2_FERTILITY"]


def main():
    d = json.loads(STATE.read_text())
    state = d["state"]
    corpus = {r["openalex"]: r for r in json.loads(CORPUS.read_text())["records"]}

    changed = Counter()
    for oid, s in state.items():
        c = corpus.get(oid)
        if not c:
            continue
        v = c["verdict"]
        if v == "FULL":
            s["status"] = "FULL_TEXT"
            s["text_chars"] = c["chars"]
        elif v == "ABSTRACT_ONLY":
            s["status"] = "ABSTRACT_ONLY"; s["job"] = "BROWSER_JOB"
            s["reason"] = "landing page only — an abstract is not a full text"
            changed["downgraded_abstract"] += 1
        else:
            s["status"] = "BOT_CHALLENGE_PAGE"; s["job"] = "BROWSER_JOB"
            s["reason"] = ("HTTP 200 bot-challenge page (Cloudflare/JS wall); "
                           "not paywalled, needs a logged-in browser")
            changed["downgraded_blocked"] += 1

    full = [s for s in state.values() if s["status"] == "FULL_TEXT"]
    todo = [s for s in state.values() if s["status"] != "FULL_TEXT"]
    bycell = defaultdict(lambda: Counter())
    for s in state.values():
        bycell[s["cell"]]["full" if s["status"] == "FULL_TEXT" else "todo"] += 1

    summary = {"ticket": "TICK-076", "primary_studies": len(state),
               "full_text": len(full),
               "rate": round(100 * len(full) / len(state), 1),
               "superseded_claim": "263 reported 108/148 = 73.0% retrieved",
               "downgraded": dict(changed),
               "outstanding": len(todo),
               "jobs": dict(Counter(s.get("job") for s in todo)),
               "by_cell": {c: {"full_text": bycell[c]["full"], "outstanding": bycell[c]["todo"],
                               "rate": round(100 * bycell[c]["full"] /
                                             max(bycell[c]["full"] + bycell[c]["todo"], 1), 1)}
                           for c in PRIORITY if c in bycell}}
    d["summary"] = summary
    STATE.write_text(json.dumps(d, indent=1))

    md = ["# A.18 full-text retrieval — state and handoff\n",
          f"**{len(full)} of {len(state)} primary studies have usable full text ({summary['rate']}%).**\n",
          "\n> **This supersedes the 73.0% figure in the first retrieval log.** That count treated "
          "any HTTP 200 with bytes as a retrieval. Converting to text showed 46 of those files were "
          "Cloudflare / JavaScript bot-challenge pages stripping to 11–303 characters, and 6 were "
          "abstract-only landing pages. They are not paywalled and not fetched: they are bot-blocked, "
          "and they belong in the browser queue.\n",
          "\n## By estimand cell — read this before the overall rate\n",
          "| cell | full text | outstanding | rate |\n|---|---|---|---|"]
    for c in PRIORITY:
        if c in bycell:
            b = summary["by_cell"][c]
            md.append(f"| `{c}` | {b['full_text']} | {b['outstanding']} | {b['rate']}% |")
    md.append("\n**`PREDICTED_RESPONSE` has 1 full text of 6 studies, and it is the only cell that "
              "can carry a demographic-significance number under Ruling 1.** That is the binding "
              "constraint on this chapter, not the overall rate.\n")
    for job, label, who in (("BROWSER_JOB", "Browser job", "a human with a logged-in browser; a proxy will NOT help"),
                            ("PROXY_JOB", "Proxy / ILL job", "UChicago proxy, ILL, or an author email")):
        rows = [s for s in todo if s.get("job") == job]
        rows.sort(key=lambda s: (PRIORITY.index(s["cell"]) if s["cell"] in PRIORITY else 99))
        md += [f"\n## {label} — {len(rows)} records\n", f"*Needs {who}. Ordered by estimand cell.*\n",
               "| cell | title | DOI | url |\n|---|---|---|---|"]
        for s in rows:
            u = (s.get("blocked_urls") or [""])[0]
            md.append(f"| `{s['cell']}` | {(s['title'] or '')[:66]} | {s.get('doi') or '—'} | {u[:66]} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
