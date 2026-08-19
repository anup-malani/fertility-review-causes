#!/usr/bin/env python3
"""
149_d3c_anchor_norm_audit.py — blast radius of the `norm()` accent-shattering defect.

D.3.c's A3 run (`148_d3c_cold_start_anchors.py`) found that the resolver's `norm()` replaced every
non-ASCII character with a SPACE instead of folding it, so an accented surname was not merely
mismatched but SPLIT, and `surnames()` then took a meaningless trailing fragment:

    "Speder"    vs index "Spéder"     -> "speder"    vs "der"
    "Fahlen"    vs index "Fahlén"     -> "fahlen"    vs "n"
    "Olah"      vs index "Oláh"       -> "olah"      vs "h"
    "Terzioglu" vs index "Terzioğlu"  -> "terzioglu" vs "lu"

The author gate then returned False — "this record HAS authors and none is ours" — which is a
confident wrong negative, not a missing-data None. `norm()` also feeds `toks()` -> `jaccard()`, so an
accented TITLE loses Jaccard against an ASCII candidate on both the gate and the score.

That resolver is INHERITED. Every chapter from B.1 onward ran a copy of it. This script measures how
far the defect reaches instead of assuming it was confined to D.3.c, per the standing rule that a fix
verified only on the cases that motivated it is verified against nothing.

Method. For each chapter's frozen `{slug}-cold-start-anchors.json`, read from whichever branch holds
it, and classify every anchor by two facts that are both recorded in the artefact:

  * does any candidate author name, or the matched record title, contain a non-ASCII character that
    the old `norm()` would have shattered?
  * did the anchor fail to verify, and if so with an authorship or title-gate reason?

An anchor that is BOTH accented AND unverified is a SUSPECT: the defect is sufficient to explain it.
An anchor that is accented and verified anyway is EXPOSED-BUT-SURVIVED — usually because the surname
happened to be ASCII while a co-author's was not, or because Crossref supplied an unaccented variant.
This is deliberately an upper bound on harm, not a re-resolution: re-running ten chapters' resolvers
against a live index would change many things at once and could not attribute the difference to this
defect. Suspects are the list an RA re-runs, one chapter at a time.

Output: literature/search-logs/despair-hopelessness-fertility-anchor-norm-audit.md
"""
import json, os, re, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, "literature", "search-logs",
                   "despair-hopelessness-fertility-anchor-norm-audit.md")

# The defect, preserved exactly, so the audit tests the code that ran rather than a description of it.
def norm_old(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    return re.sub(r"\s+", " ", s).strip()


_TRANSLIT = str.maketrans({"ø": "o", "Ø": "o", "ß": "ss", "đ": "d", "Đ": "d", "ł": "l", "Ł": "l",
                           "ı": "i", "İ": "i", "æ": "ae", "Æ": "ae", "œ": "oe", "Œ": "oe",
                           "þ": "th", "Þ": "th", "ð": "d", "Ð": "d", "ħ": "h", "ŧ": "t"})


def norm_new(s):
    s = (s or "").translate(_TRANSLIT)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def surname(n, fn):
    parts = fn(n).split()
    return parts[-1] if parts else ""


def shattered(name):
    """Would the old norm() have produced a DIFFERENT surname for this name than the fix does?"""
    return surname(name, norm_old) != surname(name, norm_new)


def branches_with(path):
    out = subprocess.run(["git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes"],
                         capture_output=True, text=True, cwd=ROOT).stdout.split()
    for ref in out:
        r = subprocess.run(["git", "cat-file", "-e", f"{ref}:{path}"], capture_output=True, cwd=ROOT)
        if r.returncode == 0:
            blob = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True,
                                  cwd=ROOT).stdout
            return ref, blob
    return None, None


SLUGS = ["evolutionary-sex-drive-contraceptive-decoupling", "child-labor-laws-and-schooling",
         "climate-anxiety-eco-doomerism", "postmaterialism-individualism-secularization",
         "caldwell-wealth-flows-westernization", "child-centeredness-intensive-parenting",
         "housing-costs", "fetal-loss-intrauterine-mortality", "antidepressants-ssri-subfecundity",
         "microplastics-pfas-reproductive"]

VERIFIED = {"verified", "verified_live_doi", "candidate_year_drift_ra_confirm",
            "expected_no_doi", "book_no_doi_expected"}


def main():
    rows, missing = [], []
    for slug in SLUGS:
        path = f"literature/search-logs/{slug}-cold-start-anchors.json"
        ref, blob = branches_with(path)
        if not blob:
            missing.append(slug)
            continue
        try:
            data = json.loads(blob)
        except Exception as e:
            missing.append(f"{slug} (unparseable: {str(e)[:40]})")
            continue
        anchors = data.get("anchors", data) if isinstance(data, dict) else data
        if not isinstance(anchors, list):
            missing.append(f"{slug} (unexpected shape)")
            continue
        for a in anchors:
            if not isinstance(a, dict):
                continue
            authors = a.get("authors") or []
            title = a.get("title") or ""
            matched = a.get("matched_title") or ""
            acc_auth = [x for x in authors if shattered(x)]
            acc_title = norm_old(matched) != norm_new(matched) and matched
            if not acc_auth and not acc_title:
                continue
            status = str(a.get("gold_status") or "")
            verified = bool(a.get("identity_verified")) or status in VERIFIED
            rows.append(dict(slug=slug, ref=(ref or "").split("/")[-1], title=title[:66],
                             authors=acc_auth, acc_title=bool(acc_title), verified=verified,
                             status=status, am=a.get("author_match")))

    L = ["# Blast-radius audit — the `norm()` accent-shattering defect", "",
         "**Raised by:** D.3.c A3 (`148_d3c_cold_start_anchors.py`), 2026-08-18. "
         "**Generated by:** `source/build/goldset/149_d3c_anchor_norm_audit.py`.", "",
         "The inherited resolver replaced every non-ASCII character with a space rather than folding "
         "it, so accented surnames were split and `surnames()` took a trailing fragment (`Spéder` -> "
         "`der`). The author gate reported that as `authors_disagree` — a confident wrong negative. "
         "The same function feeds the title gate. Every chapter from B.1 onward ran a copy of this "
         "resolver, so the question is not whether D.3.c was affected but how far the defect reaches.",
         "",
         "**This is an upper bound on harm, not a re-resolution.** An anchor is listed if the old "
         "`norm()` would have produced a different surname or title normalisation than the fix does. "
         "Re-running ten chapters against a live index would change many things at once and could not "
         "attribute the difference to this defect; the SUSPECT list is what an RA re-runs, one chapter "
         "at a time.", ""]

    if not rows:
        L += ["## Result: no exposed anchors found", "",
              "No anchor in any frozen chapter artefact carries an author name or matched title that "
              "the old `norm()` would have normalised differently. On the evidence in the artefacts, "
              "the defect's realised blast radius is confined to D.3.c, whose primary cell is a "
              "Bulgarian-Hungarian research family and therefore the first corpus to hit it. The "
              "defect was real and is fixed; it appears not to have cost an anchor before now.", ""]
    else:
        # An unverified anchor is only ATTRIBUTABLE to this defect if the author gate actually
        # compared surnames and said no — `author_match is False`. `None` is the missing-metadata
        # state: the record carried no authors, so the shattered surname was never used, and the
        # failure belongs to some other gate (in practice the book-canon one). Collapsing None into
        # the suspect list would overstate the damage in exactly the direction an author of the fix
        # is tempted to overstate it.
        exposed_unverified = [r for r in rows if not r["verified"]]
        susp = [r for r in exposed_unverified if r["am"] is False]
        unattributable = [r for r in exposed_unverified if r["am"] is not False]
        L += [f"## Result: {len(rows)} exposed anchors across "
              f"{len({r['slug'] for r in rows})} chapters; **{len(susp)} SUSPECT**", "",
              "| Chapter | Anchor | Accented authors | Accented title | Verified | Status |",
              "|---|---|---|---|---|---|"]
        for r in sorted(rows, key=lambda x: (x["verified"], x["slug"])):
            L.append(f"| {r['slug'][:26]} | {r['title'][:44]} | "
                     f"{', '.join(r['authors'])[:34] or '—'} | {'yes' if r['acc_title'] else '—'} | "
                     f"{'yes' if r['verified'] else '**NO**'} | {r['status'][:26]} |")
        L += ["", "### Suspects — re-run these anchors against the fixed resolver", ""]
        if susp:
            for r in susp:
                L.append(f"- **{r['slug']}** — {r['title']} "
                         f"(authors {', '.join(r['authors']) or 'n/a'}; author_match=False)")
        else:
            L.append("**None.** No unverified exposed anchor has `author_match == False`, which is "
                     "the only state this defect can produce. Where an exposed anchor verified, the "
                     "matching surname was ASCII or the index supplied an unaccented variant; where "
                     "one did not verify, the gate never compared surnames at all.")
        L.append("")
        if unattributable:
            L += ["### Exposed, unverified, but NOT attributable to this defect", "",
                  "These carry an accented name and did not verify, but their author gate returned "
                  "`None` — the record had no author metadata, so the shattered surname was never "
                  "compared. Their failure belongs to another gate, in practice the book-canon one, "
                  "and re-running them against the fix will not change them.", ""]
            for r in unattributable:
                L.append(f"- **{r['slug']}** — {r['title']} "
                         f"(authors {', '.join(r['authors']) or 'n/a'}; author_match={r['am']}; "
                         f"status `{r['status']}`)")
            L.append("")

    if missing:
        L += ["## Chapters whose artefact could not be read", "",
              "Listed so an unread file is never mistaken for a clean one.", ""]
        L += [f"- {m}" for m in missing] + [""]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(L) + "\n")
    n_att = len([r for r in rows if not r["verified"] and r["am"] is False])
    print(f"wrote {OUT}  ({len(rows)} exposed, {n_att} attributable suspect, {len(missing)} unreadable)")


if __name__ == "__main__":
    main()
