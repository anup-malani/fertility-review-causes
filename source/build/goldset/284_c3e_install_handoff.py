#!/usr/bin/env python3
"""284 — C.3.e: install hand-retrieved PDFs by CONTENT, never by filename. TICK-077.

Hand-retrieved PDFs arrive publisher-named: `749desai.pdf`, `1-s2.0-S0304387815000061-main.pdf`,
two files both called `EBSCO-FullText-09_01_2026.pdf`. Installing those by guessing from the
filename is how a wrong pairing enters the extraction table and stays there silently -- every
number downstream would then be attributed to the wrong study.

So each PDF is matched on its OWN first-page text against the eight expected records, scored on
title-token overlap plus first-author surname plus year. A file that does not win a target
clearly is left UNMATCHED for a human read rather than being forced onto the nearest key.

Usage: python3 284_c3e_install_handoff.py [--src DIR]
"""
import csv, json, re, subprocess, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
DEST = ROOT / "temp" / "c3e-handoff"
SRC = Path(sys.argv[sys.argv.index("--src") + 1]).expanduser() if "--src" in sys.argv \
    else Path.home() / "Downloads" / "c3e"


def fold(s):
    s = (s or "").lower().replace("’", "'")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def toks(s):
    return [t for t in fold(s).split() if len(t) > 2]


STOP = {"the", "and", "for", "from", "with", "evidence", "impact", "effect", "effects",
        "does", "using", "data", "case", "study", "programs", "program"}


def head_text(pdf, pages=3):
    r = subprocess.run(["pdftotext", "-q", "-f", "1", "-l", str(pages), "-enc", "UTF-8",
                        str(pdf), "-"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def main():
    targets = list(csv.DictReader(open(LOGS / "credit-constraints-retrieval-handoff.csv")))
    anchors = {a["key"]: a for a in
               json.loads((LOGS / "credit-constraints-cold-start-anchors.json").read_text())}
    for t in targets:
        a = anchors.get(t["key"])
        t["first_author"] = ((a or {}).get("top_candidate") or {}).get("authors_first") or ""

    pdfs = sorted(p for p in SRC.glob("*.pdf"))
    print(f"{len(pdfs)} PDFs in {SRC}, {len(targets)} expected records\n")
    DEST.mkdir(parents=True, exist_ok=True)

    scores = {}
    for p in pdfs:
        txt = head_text(p)
        if not txt.strip():
            scores[p.name] = []
            print(f"  !! {p.name}: no extractable text (scanned image?)")
            continue
        ft = fold(txt)
        row = []
        for t in targets:
            tt = [w for w in toks(t["title"]) if w not in STOP]
            if not tt:
                continue
            overlap = sum(1 for w in set(tt) if w in ft) / len(set(tt))
            surname = toks(t["first_author"])[-1] if t["first_author"] else ""
            auth = 1 if surname and surname in ft else 0
            yr = 1 if t["year"] and t["year"] in txt[:6000] else 0
            row.append((round(overlap + 0.35 * auth + 0.15 * yr, 3), round(overlap, 3),
                        auth, yr, t["key"]))
        row.sort(reverse=True)
        scores[p.name] = row

    # greedy one-to-one assignment on the best mutual scores
    assigned, used_keys, used_files = {}, set(), set()
    flat = sorted(((r[0], f, r[4], r) for f, rows in scores.items() for r in rows[:3]),
                  reverse=True)
    for total, fname, key, r in flat:
        if fname in used_files or key in used_keys or total < 0.55:
            continue
        assigned[key] = (fname, r)
        used_files.add(fname)
        used_keys.add(key)

    print("MATCHES (score = title overlap + 0.35*author + 0.15*year)")
    installed = []
    for t in targets:
        k = t["key"]
        if k in assigned:
            fname, r = assigned[k]
            dst = DEST / f"{k}.pdf"
            dst.write_bytes((SRC / fname).read_bytes())
            installed.append({"key": k, "src": fname, "total": r[0], "title_overlap": r[1],
                              "author_hit": bool(r[2]), "year_hit": bool(r[3]),
                              "installed": str(dst.relative_to(ROOT))})
            print(f"  OK  {k:26s} <- {fname[:52]:52s} {r[0]:.2f} "
                  f"(title {r[1]:.2f}, author {'Y' if r[2] else 'n'}, year {'Y' if r[3] else 'n'})")
        else:
            installed.append({"key": k, "src": None, "installed": None})
            print(f"  --  {k:26s} NO PDF MATCHED")
    left = [f for f in scores if f not in used_files]
    for f in left:
        top = scores[f][0] if scores[f] else None
        print(f"  ??  UNMATCHED FILE {f[:56]} best={top}")

    (LOGS / "credit-constraints-handoff-install.json").write_text(
        json.dumps({"src": str(SRC), "installed": installed,
                    "unmatched_files": left}, indent=2))
    print(f"\ninstalled {sum(1 for i in installed if i['installed'])} of {len(targets)}")


if __name__ == "__main__":
    main()
