#!/usr/bin/env python3
"""343 — install hand-retrieved PDFs for C.2.f, matched BY CONTENT (TICK-081).

Hand-retrieved PDFs arrive publisher-named (`EBSCO-FullText-09_08_2026.pdf`,
`05E53C072D3948BDA9AEF3723DC3CF35.pdf`), so the filename carries no information about which record
they are. Installing on filename order, or on a human's say-so, silently corrupts the extraction
table (`handoff-file-match-by-content`).

**The matching rule is contiguous title containment, not token overlap, and that is not fussiness.**
The first version of this matcher accepted a record at 0.80 token overlap with no contiguous match.
It paired *Gendered fertility intentions and child schooling: insights on the quantity-quality
trade-off from Ethiopia* (J. Demographic Economics 2025) with C2F0844 *Marital Fertility and
Investment in Children's Education* — two different papers sharing only the generic words fertility,
investment, children and education. A wrong pairing here is worse than a missing file, because it
enters the extraction table looking correct.

So a file is installed only if the record's title (or, for a bilingual title, one side of it) appears
as a contiguous normalised string in the PDF's first pages. Everything else is reported UNMATCHED
with the PDF's opening line, for a human to read.

Uses the canonical `source/lib/textnorm.py` fold (TICK-074), not a local copy.
"""
import json, re, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
from textnorm import norm                                            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
PDFS = ROOT / "literature" / "pdfs" / "rising-inequality-and-status-competition"
RETR = LOGS / "rising-inequality-and-status-competition-retrieval.json"
GOT = {"fetched", "already_on_disk", "covered_by_twin"}


def head_text(p, pages=4):
    r = subprocess.run(["pdftotext", "-f", "1", "-l", str(pages), "-q", str(p), "-"],
                       capture_output=True, text=True)
    return norm(r.stdout or "")


def title_variants(t):
    """A bilingual title like '補習、生育與階級流動;Shadow Education...' has two sides; either may
    be the one printed in the PDF."""
    parts = [p for p in re.split(r"[;；|]", t or "") if p.strip()]
    return [p for p in ([t] + parts) if len(norm(p)) >= 18]


def main():
    src = pathlib.Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else \
        pathlib.Path.home() / "Downloads" / "c2f"
    if not src.is_dir():
        sys.exit(f"no such directory: {src}")
    data = json.loads(RETR.read_text())
    outstanding = [r for r in data["records"] if r["status"] not in GOT]
    files = sorted(p for p in src.iterdir() if p.suffix.lower() == ".pdf")
    PDFS.mkdir(parents=True, exist_ok=True)

    installed, unmatched, claimed = [], [], {}
    for p in files:
        txt = head_text(p)
        hit = None
        for rec in outstanding:
            for v in title_variants(rec.get("title")):
                nv = norm(v)
                if nv and nv[:70] in txt:
                    hit = (rec, v)
                    break
            if hit:
                break
        if not hit:
            raw = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "-q", str(p), "-"],
                                 capture_output=True, text=True).stdout
            unmatched.append((p.name, " ".join(raw.split())[:130]))
            continue
        rec, v = hit
        if rec["screen_id"] in claimed:
            unmatched.append((p.name, f"second file claiming {rec['screen_id']} "
                                      f"(already {claimed[rec['screen_id']]})"))
            continue
        dest = PDFS / f"{rec['screen_id']}.pdf"
        dest.write_bytes(p.read_bytes())
        claimed[rec["screen_id"]] = p.name
        rec["status"] = "hand_retrieved"
        rec["path"] = str(dest.relative_to(ROOT))
        rec["handoff"] = None
        rec["installed_from"] = p.name
        installed.append((rec["screen_id"], rec.get("cell"), p.name))

    RETR.write_text(json.dumps(data, indent=1) + "\n")

    print(f"installed {len(installed)} of {len(files)} files\n")
    for sid, cell, name in installed:
        print(f"  {sid}  {cell:32s} <- {name[:52]}")
    if unmatched:
        print(f"\nUNMATCHED ({len(unmatched)}) — not installed, read these:")
        for name, why in unmatched:
            print(f"  {name[:56]}\n      {why}")

    still = [r for r in data["records"] if r["status"] not in GOT | {"hand_retrieved"}]
    print(f"\nstill outstanding: {len(still)}")
    for r in still:
        print(f"  {r['screen_id']}  [{r.get('handoff')}]  {(r.get('title') or '')[:64]}")

    PRIMARY = {"DISPERSION_FERTILITY", "POSITIONAL_ALLOCATION_FERTILITY",
               "REQUIRED_INVESTMENT_FERTILITY", "TUTORING_POLICY_FERTILITY"}
    print("\nPRIMARY CELL coverage after install:")
    for c in sorted(PRIMARY):
        rs = [r for r in data["records"] if r.get("cell") == c]
        g = sum(1 for r in rs if r["status"] in GOT | {"hand_retrieved"})
        print(f"    {g}/{len(rs)}  {c}{'   <-- COMPLETE' if rs and g == len(rs) else ''}")


if __name__ == "__main__":
    main()
