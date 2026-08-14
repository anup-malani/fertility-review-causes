#!/usr/bin/env python3
"""
143_b6_fulltext_probe.py — B.6, stage 6 prep. Locate the methods facts before hand-coding them.

The search scope committed, in advance, to four fields that a title/abstract screen CANNOT assign and
that full text must settle: `PARITY_HANDLING`, `BLANK_CONTROL`, `MIXTURE_SEPARABLE` and
`ESTIMAND_LEVEL`. This script does not decide any of them. It finds and quotes the sentences where
each is likely to be stated, per document, so that the hand-coding in the next stage is guided by
located evidence rather than by recall, and so a second reader can check the judgement against the
same passages.

Why this exists as a separate step. Extraction on this chapter turns almost entirely on
`PARITY_HANDLING` — PFAS leave the body through pregnancy, lactation and menstruation, so parity
causes exposure, and an estimate that does not handle it is close to uninterpretable (Call 2). That
is a methods fact buried in a methods section, and reading 53 documents for it unaided is exactly the
task where a reader's attention degrades and a null gets recorded because a phrase was missed rather
than because it was absent. A located quotation is checkable; "I read it" is not.

The distinction this preserves, which matters for the two-track synthesis:
    NOT FOUND  — the probe found no matching passage. It is a prompt to read, never a verdict.
    FOUND      — a passage exists and is quoted. The human decides what it means.
A field with no hits is reported as unresolved, not as absent, for the same reason the reconnaissance
kept failed requests out of its zero counts.

Output: extraction/{slug}-fulltext-probe.csv        (one row per document per field hit)
        literature/search-logs/{slug}-fulltext-probe.md
"""
import csv, os, re

SLUG = "microplastics-pfas-reproductive"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
LOG1 = os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log.csv")
GATE = os.path.join(EXTRACT, f"{SLUG}-ra-gate.csv")
OUT_CSV = os.path.join(EXTRACT, f"{SLUG}-fulltext-probe.csv")
OUT_MD = os.path.join(LOGS, f"{SLUG}-fulltext-probe.md")

# Each field lists the phrases whose PRESENCE means the methods section is discussing it. Deliberately
# broad: a false hit costs one sentence of reading, a miss costs a mis-coded field.
FIELDS = {
    "PARITY_HANDLING": [
        r"nullipar\w*", r"primipar\w*", r"\bparous\b", r"\bparity\b", r"parity[- ]stratified",
        r"conditioning on parity", r"parity[- ]conditioning", r"previous pregnanc\w+",
        r"gravidity", r"first pregnancy", r"restricted to women who had never",
    ],
    "EXPOSURE_TIMING": [
        r"preconception", r"pre[- ]pregnancy", r"prior to conception", r"before conception",
        r"first trimester", r"early pregnancy", r"at enrol\w+", r"baseline sample",
    ],
    "BLANK_CONTROL": [
        r"procedural blank", r"\bblank\w*\b", r"contamination control", r"quality assurance",
        r"quality control", r"cleanroom", r"laminar flow", r"cotton lab coat", r"glass\w* only",
        r"airborne contamination",
    ],
    "MIXTURE_SEPARABLE": [
        r"compound[- ]specific", r"individual compound", r"single[- ]pollutant model",
        r"mixture model", r"weighted quantile", r"\bWQS\b", r"\bBKMR\b", r"quantile g[- ]computation",
        r"principal component", r"co[- ]exposure",
    ],
    "ESTIMAND_LEVEL": [
        r"fecundability ratio", r"time to pregnancy", r"time[- ]to[- ]pregnancy", r"\bTTP\b",
        r"cycles? of attempt", r"completed fertility", r"total fertility rate",
        r"number of (live )?births", r"parity at", r"hazard ratio", r"odds ratio",
    ],
    "SAMPLING_FRAME": [
        r"in vitro fertil\w+", r"\bIVF\b", r"\bICSI\b", r"fertility clinic", r"assisted reproduct\w+",
        r"general population", r"population[- ]based", r"occupational cohort", r"birth cohort",
        r"volunteers", r"convenience sample",
    ],
    "REVERSE_CAUSATION_AWARE": [
        r"reverse caus\w+", r"excret\w+", r"elimination", r"menstrual (blood )?loss",
        r"breastfeed\w+", r"lactation", r"transplacental", r"pharmacokinetic\w*",
        r"half[- ]life",
    ],
}
CONTEXT = 190       # characters of quoted context around a hit
MAX_QUOTES = 2      # per field per document; enough to judge, short enough to read


def sentences_around(text, pattern):
    out = []
    for m in re.finditer(pattern, text, flags=re.I):
        a = max(0, m.start() - CONTEXT // 2)
        b = min(len(text), m.end() + CONTEXT // 2)
        frag = re.sub(r"\s+", " ", text[a:b]).strip()
        out.append(frag)
        if len(out) >= MAX_QUOTES:
            break
    return out


def main():
    readable = {}
    for f in sorted(os.listdir(PDF_DIR)):
        if f.endswith(".txt") and os.path.getsize(os.path.join(PDF_DIR, f)) > 500:
            readable[f.split("__")[0]] = os.path.join(PDF_DIR, f)

    rows = list(csv.DictReader(open(LOG1)))
    gate = {r["openalex_id"]: r for r in csv.DictReader(open(GATE))}
    targets = [r for r in rows if r["job"] in ("A_primary", "A2_input")
               and r["openalex_id"] in readable]

    out_rows, per_doc = [], []
    for r in targets:
        wid = r["openalex_id"]
        text = open(readable[wid], errors="ignore").read()
        g = gate.get(wid, {})
        found = {}
        for field, pats in FIELDS.items():
            quotes = []
            for p in pats:
                quotes += sentences_around(text, p)
                if len(quotes) >= MAX_QUOTES:
                    break
            found[field] = quotes[:MAX_QUOTES]
            for q in found[field]:
                out_rows.append([wid, r["doi"], g.get("cell", ""), r["chemical_family"], field, q])
            if not found[field]:
                out_rows.append([wid, r["doi"], g.get("cell", ""), r["chemical_family"], field,
                                 "NOT FOUND — read the document; this is a prompt, not a verdict"])
        per_doc.append((r, g, found, len(text)))

    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["openalex_id", "doi", "cell", "chemical_family", "field", "evidence"])
        w.writerows(out_rows)

    # Coverage: how often each field is even discussed. This is the number that says whether the
    # two-track synthesis is feasible before anyone tries to build it.
    cov = {f: 0 for f in FIELDS}
    for _, _, found, _ in per_doc:
        for f, q in found.items():
            if q:
                cov[f] += 1
    n = len(per_doc)

    L = [f"# Full-text probe — {SLUG} (B.6)", "",
         "Generated by `source/build/goldset/143_b6_fulltext_probe.py`. This locates evidence; it "
         "decides nothing. Every field below is hand-coded in the next stage, and the quotations "
         "here are what a second reader checks that coding against.", "",
         f"**{n} documents probed** — every primary-cell and fertility-input record whose full text "
         "is held.", "",
         "## Field coverage — is the two-track synthesis feasible?", "",
         "`PARITY_HANDLING` is the one that matters. PFAS leave the body through pregnancy, lactation "
         "and menstruation, so parity causes exposure; Call 2 restricts the primary synthesis to "
         "estimates that handle it. If few documents even discuss parity, the restricted track is "
         "too thin to pool and the chapter reports narratively — a decision that should be made from "
         "this table rather than discovered halfway through extraction.", "",
         "| field | documents discussing it | share |", "|---|---|---|"]
    for f in FIELDS:
        L.append(f"| `{f}` | {cov[f]}/{n} | {cov[f] / max(n, 1):.0%} |")
    L += ["",
          "A field with no hits is **unresolved, not absent**. The probe searches a fixed phrase "
          "list; a paper that handles parity in wording the list does not carry will read as NOT "
          "FOUND and must still be read.", "",
          "## Per document", ""]
    for r, g, found, ln in sorted(per_doc, key=lambda x: (x[1].get("cell", ""),
                                                          -(int(x[0].get("cited_by", 0) or 0)))):
        L += [f"### {r['title'][:96]}", "",
              f"`{r['doi'] or 'no doi'}` · `{g.get('cell', '?')}` · family `{r['chemical_family']}` "
              f"· {ln // 1000}k chars", ""]
        for f in FIELDS:
            q = found[f]
            if q:
                L.append(f"- **{f}** — " + " … ".join(f"“…{x}…”" for x in q))
            else:
                L.append(f"- **{f}** — *not found; read the document*")
        L.append("")
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"documents={n} rows={len(out_rows)}")
    for f in FIELDS:
        print(f"  {f:<26} {cov[f]}/{n} ({cov[f] / max(n, 1):.0%})")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
