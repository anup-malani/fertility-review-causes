#!/usr/bin/env python3
"""Build and maintain the shared literature folder in Dropbox.

The folder is the single home for PDFs. One subfolder per hypothesis, named
<code>-<slug>, where both come from HYPOTHESES-v5.md so nothing is typed by hand.

Codes are unstable: A.10/B.4/B.15 in the 2026-07 handoffs are A.11/C.3.b/C.3.c in
the current master list. That is why folder names are generated rather than
authored, and why this script can rename a folder when a code moves without
touching its contents.

  python3 source/build/sync_lit_folders.py            # active hypotheses only
  python3 source/build/sync_lit_folders.py --all      # every non-deprecated one
  python3 source/build/sync_lit_folders.py --dry-run

Never deletes. Renames only when it finds exactly one existing folder whose slug
matches and whose code does not.
"""
import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
MASTER = REPO / "HYPOTHESES-v5.md"
LIT_ROOT = pathlib.Path(
    "/Users/amalani/UChicago Law Dropbox/Anup Malani/fertility/fertility-review-lit"
)

# Hypotheses with a chapter drafted, in progress, or screened.
ACTIVE = {
    "tempo-effects-birth-postponement",
    "child-labor-laws-and-schooling",
    "evolutionary-sex-drive-contraceptive-decoupling",
    "old-age-security-pension-crowdout",
    "climate-anxiety-eco-doomerism",
}

HEADING = re.compile(r"^#{3,4}\s+([A-E]\.\d+(?:\.[a-z])?)\.?\s+(.*)$")
SLUG = re.compile(r"^-\s+\*\*slug:\*\*\s+`([^`]+)`")
TAG = re.compile(r"\s*\[(NEW v5|DEPRECATED|NARROWED v5)\]\s*")


def parse_master(path=MASTER):
    rows, cur = [], None
    for line in path.read_text().split("\n"):
        m = HEADING.match(line.strip())
        if m:
            title = TAG.sub("", m.group(2)).strip()
            cur = {
                "code": m.group(1),
                "title": title.strip("~"),
                "slug": None,
                "deprecated": "DEPRECATED" in line or title.startswith("~~"),
            }
            rows.append(cur)
            continue
        m = SLUG.match(line.strip())
        if m and cur is not None and cur["slug"] is None:
            cur["slug"] = m.group(1)
    return [r for r in rows if r["slug"]]


README = """# fertility-review-lit — where the PDFs live

This is the one home for papers in the fertility-explanations systematic review.
If a PDF is not here, it does not exist as far as the review is concerned.

## Where to put a paper

One folder per hypothesis, named `<code>-<slug>`. Put the paper in the folder for
the hypothesis it is evidence about. If a paper is evidence for two hypotheses,
put it in both — disk is cheap and a missing paper is expensive.

If the folder you need does not exist yet, create it using the exact name in
`_INDEX.md`. Do not invent a name.

## How to name a paper

    <authors>-<year>-<what-it-measures>.pdf

**Authors.** Surnames, lowercased, joined by dashes. One or two authors, use
both. Three or more, use the first plus `-etal`.

    von-rueden-jaeggi-2016-...
    danzer-zyska-2023-...
    lei-etal-2026-...

**Year.** Four digits. If the same authors have two papers in the same year, add
a letter matching the bibliography: `cigno-rosati-2024a`, `cigno-rosati-2024b`.

**What it measures.** Eight words or fewer, dashes between them. Describe the
paper's *subject, setting, and design* — not what it concluded.

    GOOD  von-rueden-jaeggi-2016-status-fertility-33-nonindustrial-societies.pdf
    GOOD  danzer-zyska-2023-brazil-rural-pension-expansion-fertility.pdf
    GOOD  bisi-sturm-van-bavel-2024-climate-vignette-experiment-fertility-desires.pdf

    BAD   von-rueden-jaeggi-2016-status-strongly-predicts-fertility.pdf
    BAD   danzer-zyska-2023-pensions-reduce-births.pdf

**Why the finding does not go in the filename.** A filename is sticky: once it is
written it gets cited in notes and nobody re-reads it. This review has already
been bitten by exactly that. A claim that one side of a comparison "rests on a
single study" was carried across four drafts of the contraceptive-decoupling
chapter as settled fact and turned out to be false — four more studies were
sitting unused in our own extraction file, and pooling them reversed the sign of
the headline result. A filename asserting a finding is the same failure waiting
to happen, and it is worse in a systematic review, because whoever opens the
folder reads the conclusion before the method.

Describing the subject gives you everything useful about skimming a folder and
none of the risk. You can still tell at a glance why you would open the file.

**Working papers and versions.** Add `-working-paper` or `-preprint` at the end if
the PDF is not the published version.

## What else goes in a hypothesis folder

Only PDFs and, if you have them, the paper's supplementary files. Extraction
spreadsheets, notes, and screening logs stay in the git repository, not here.

## Questions

Ask Anup. Do not guess at a folder name — a paper filed under the wrong
hypothesis is harder to find than one that was never downloaded.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="create a folder for every non-deprecated hypothesis")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not MASTER.exists():
        sys.exit(f"master list not found: {MASTER}")
    rows = parse_master()
    live = [r for r in rows if not r["deprecated"]]
    wanted = live if args.all else [r for r in live if r["slug"] in ACTIVE]

    if not LIT_ROOT.parent.exists():
        sys.exit(f"Dropbox fertility folder not found: {LIT_ROOT.parent}")

    existing = {}
    if LIT_ROOT.exists():
        for d in LIT_ROOT.iterdir():
            if d.is_dir() and "-" in d.name:
                code, _, slug = d.name.partition("-")
                existing.setdefault(slug, []).append(d)

    created, renamed, kept = [], [], []
    for r in wanted:
        name = f"{r['code']}-{r['slug']}"
        target = LIT_ROOT / name
        if target.exists():
            kept.append(name)
            continue
        prior = existing.get(r["slug"], [])
        if len(prior) == 1:
            renamed.append((prior[0].name, name))
            if not args.dry_run:
                prior[0].rename(target)
        else:
            created.append(name)
            if not args.dry_run:
                target.mkdir(parents=True, exist_ok=True)

    if not args.dry_run:
        LIT_ROOT.mkdir(parents=True, exist_ok=True)
        (LIT_ROOT / "_README.md").write_text(README)
        idx = ["# Index — hypothesis code to folder name",
               "",
               "Generated from `HYPOTHESES-v5.md` by `source/build/sync_lit_folders.py`.",
               "Do not edit by hand; codes change and this file is regenerated.",
               "",
               "A folder marked **created** exists. Any other row is a folder you may",
               "create when you have a paper for it, using exactly the name given.",
               "",
               "| Code | Folder name | Hypothesis | Folder exists |",
               "|---|---|---|---|"]
        have = {p.name for p in LIT_ROOT.iterdir() if p.is_dir()} if LIT_ROOT.exists() else set()
        for r in live:
            name = f"{r['code']}-{r['slug']}"
            idx.append(f"| {r['code']} | `{name}` | {r['title']} | "
                       f"{'created' if name in have else ''} |")
        dep = [r for r in rows if r["deprecated"]]
        if dep:
            idx += ["", "## Deprecated — do not file papers here", "",
                    "| Code | Hypothesis |", "|---|---|"]
            idx += [f"| {r['code']} | {r['title']} |" for r in dep]
        (LIT_ROOT / "_INDEX.md").write_text("\n".join(idx) + "\n")
        (REPO / "temp").mkdir(exist_ok=True)
        (REPO / "temp" / "hypothesis-codes.json").write_text(json.dumps(rows, indent=1))

    print(f"lit root: {LIT_ROOT}")
    print(f"  {len(live)} live hypotheses in master list, {len(wanted)} folders wanted")
    for n in created:
        print(f"  created  {n}")
    for old, new in renamed:
        print(f"  renamed  {old}  ->  {new}")
    for n in kept:
        print(f"  ok       {n}")
    if args.dry_run:
        print("  (dry run, nothing written)")


if __name__ == "__main__":
    main()
