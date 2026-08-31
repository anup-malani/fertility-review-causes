#!/usr/bin/env python3
"""268 — A.18: recover TABLE bodies from PMC full XML. TICK-076.

BioC won this chapter's retrieval, but it returns body text and **drops table
bodies**. On the Genotype x Cohort paper the BioC text says "Table 1 reports the
parameter estimates" and contains not one of them. Since heritability estimates,
their standard errors and their cohort interactions live almost entirely in
tables, that makes BioC excellent for screening and insufficient for extraction.

PMC's efetch XML carries `<table-wrap>` elements in full. This appends them to the
text corpus so extraction reads the numbers rather than a reference to them.

**A second defect this exposed:** behaviour-genetics papers write coefficients
**without a leading zero** — `.350 (.424)`, `.498 (.105)***`. Any pattern anchored
on `0\\.` misses every one of them and reports a table-rich paper as numberless.
The harvest patterns in 266 are leading-zero-optional; the diagnostic used to
check them was not, which is how this hid.

Usage: python3 source/build/goldset/268_a18_pmc_tables.py
"""
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
TXT = TEMP / "text"
OUT = LOGS / "heritability-fertility-genetic-pmc-tables.json"
EFETCH = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
          "?db=pmc&id={}&rettype=xml")
NUM = re.compile(r"(?<![\d.])[-−]?\d*\.\d{2,5}(?![\d])")


def main():
    pmc = json.loads((LOGS / "heritability-fertility-genetic-pmc-recovery.json").read_text())
    recs = [r for r in pmc["records"] if r.get("pmcid")]
    print(f"PMC records available: {len(recs)}")
    rows, appended = [], 0
    for r in recs:
        oid, pmcid = r["openalex"], r["pmcid"]
        tf = TXT / f"{oid}.txt"
        if not tf.exists():
            rows.append({"openalex": oid, "pmcid": pmcid, "status": "NO_BASE_TEXT"})
            continue
        p = subprocess.run(["curl", "-sSL", "--max-time", "90",
                            EFETCH.format(pmcid.replace("PMC", ""))],
                           capture_output=True, text=True)
        xml = p.stdout or ""
        tables = re.findall(r"<table-wrap.*?</table-wrap>", xml, re.S)
        if not tables:
            rows.append({"openalex": oid, "pmcid": pmcid, "status": "NO_TABLES",
                         "xml_bytes": len(xml)})
            time.sleep(0.4)
            continue
        chunks = []
        for t in tables:
            txt = re.sub(r"<[^>]+>", " ", t)
            txt = re.sub(r"&[a-z]+;", " ", txt)
            chunks.append(re.sub(r"[ \t]+", " ", txt).strip())
        block = "\n\n=== PMC TABLES ===\n\n" + "\n\n".join(chunks)
        base = tf.read_text()
        if "=== PMC TABLES ===" not in base:
            tf.write_text(base + block)
            appended += 1
        nnum = len(NUM.findall(block))
        rows.append({"openalex": oid, "pmcid": pmcid, "status": "TABLES_APPENDED",
                     "n_tables": len(tables), "table_chars": len(block),
                     "decimal_values_in_tables": nnum})
        time.sleep(0.4)

    from collections import Counter
    st = Counter(r["status"] for r in rows)
    withnum = [r for r in rows if r.get("decimal_values_in_tables", 0) > 0]
    OUT.write_text(json.dumps({"summary": {
        "ticket": "TICK-076", "pmc_records": len(recs), "status": dict(st),
        "texts_appended": appended,
        "records_with_table_numbers": len(withnum),
        "median_decimals_per_record": sorted(r["decimal_values_in_tables"] for r in withnum)[len(withnum)//2] if withnum else 0,
        "note": "BioC returns body text but drops table bodies; estimates live in tables. "
                "Numbers are written WITHOUT a leading zero (.350), so any 0\\\\. anchored "
                "pattern reports a table-rich paper as numberless."},
        "records": rows}, indent=1))
    print("status:", dict(st))
    print(f"texts appended: {appended}   records with table numbers: {len(withnum)}")


if __name__ == "__main__":
    main()
