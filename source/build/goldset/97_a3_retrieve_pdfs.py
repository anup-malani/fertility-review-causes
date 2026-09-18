#!/usr/bin/env python3
"""
97_a3_retrieve_pdfs.py — A.3, automated open-access PDF retrieval for the pooling set.

Reuses the D.3.b/B.1 retrieval engine (step 82): OpenAlex all-locations + Unpaywall fallback +
Europe PMC + derived landing-page constructions, %PDF magic-byte verified, idempotent. The engine's
pure helpers are imported from 82 rather than copied.

A.3 specifics:
  * ONE pooling file (`output/diffusion-of-fertility-control-estimand-ready.json`, 252 records).
  * Priority is the 44-study IDENTIFIED CORE (identification_of_diffusion == SEPARATES_FROM_COMMON_SHOCK)
    ahead of the 194 descriptive-residual records. The chapter's synthesis turns on the identified core,
    so its retrieval rate is reported SEPARATELY — a union-only rate would hide a gap in exactly the
    stratum that matters (the failure that capped B.1 at 20/95).
  * Automated OA only. Non-OA and browser-blocked records are split into a human handoff by access
    class (closed = needs UChicago proxy/ILL; oa_but_blocked = free but refuses a non-browser client).

Outputs:
  literature/pdfs/diffusion-of-fertility-control/{WID}__{slug}.pdf  (gitignored)
  extraction/diffusion-of-fertility-control-pdf-retrieval-log.csv
  extraction/diffusion-of-fertility-control-missing-pdf-dois.csv    (human handoff)
"""
import csv, importlib.util, json, time
from pathlib import Path

SLUG = "diffusion-of-fertility-control"
ROOT = Path(__file__).resolve().parents[3]
POOL = ROOT / "output" / f"{SLUG}-estimand-ready.json"
PDF_DIR = ROOT / "literature" / "pdfs" / SLUG
LOG = ROOT / "extraction" / f"{SLUG}-pdf-retrieval-log.csv"
MISSING = ROOT / "extraction" / f"{SLUG}-missing-pdf-dois.csv"
SEP = "SEPARATES_FROM_COMMON_SHOCK"


def _engine():
    path = Path(__file__).resolve().parent / "82_d3b_retrieve_pdfs.py"
    spec = importlib.util.spec_from_file_location("d3b_retrieve_engine", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


E = _engine()


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    pool = json.load(open(POOL))
    for r in pool:
        r["_identified"] = (r.get("identification_of_diffusion") or "").upper() == SEP
    pool.sort(key=lambda r: (0 if r["_identified"] else 1, -(r.get("year") or 0)))

    work_ids = [x["paperId"] for x in pool if str(x.get("paperId", "")).startswith("W")]
    meta = E.openalex_batch(work_ids)

    rows = []
    for x in pool:
        wid = x.get("paperId", "")
        w = meta.get(wid, {})
        oa = w.get("open_access") or {}
        doi = x.get("doi") or ""
        dest = PDF_DIR / f"{wid}__{E.slugify(x.get('title',''))}.pdf"
        status, detail, size, used_url = "no_oa_url", "", 0, ""
        if dest.exists():
            status, detail, size = "already_present", "skip", dest.stat().st_size
        else:
            up = E.unpaywall(doi)
            urls = E.candidate_urls(w, up, doi)
            tried = []
            for url in urls[:10]:
                ok, why = E.download(url, dest)
                tried.append(why)
                if ok:
                    status, detail, size, used_url = "downloaded", "ok", dest.stat().st_size, url
                    break
                time.sleep(0.2)
            if status != "downloaded":
                status = "failed" if urls else "no_oa_url"
                detail = ",".join(dict.fromkeys(tried)) if tried else "closed"
            time.sleep(0.2)
        rows.append({"work_id": wid, "doi": doi,
                     "stratum": "identified_core" if x["_identified"] else "descriptive_residual",
                     "cell": x.get("cell"), "year": x.get("year"), "venue": x.get("venue") or "",
                     "oa_status": oa.get("oa_status") or "closed", "pdf_url": used_url,
                     "download_status": status, "detail": detail, "bytes": size,
                     "file": dest.name if status in ("downloaded", "already_present") else "",
                     "title": (x.get("title") or "")[:120]})

    with open(LOG, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wtr.writeheader(); wtr.writerows(rows)

    missing = [r for r in rows if not r["file"]]
    fields = ["stratum", "access_class", "doi", "work_id", "year", "venue", "detail", "title"]
    with open(MISSING, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=fields)
        wtr.writeheader()
        for r in sorted(missing, key=lambda r: (r["stratum"] != "identified_core",
                                                r["oa_status"] == "closed")):
            access = "closed" if r["oa_status"] == "closed" else "oa_but_blocked"
            wtr.writerow({**{k: r[k] for k in fields if k != "access_class"}, "access_class": access})

    def rate(pred):
        sel = [r for r in rows if pred(r)]
        return sum(1 for r in sel if r["file"]), len(sel)
    ic_got, ic_n = rate(lambda r: r["stratum"] == "identified_core")
    all_got, all_n = rate(lambda r: True)
    print(f"identified core: {ic_got}/{ic_n} retrieved")
    print(f"full pooling set: {all_got}/{all_n} retrieved")
    print(f"missing: {len(missing)} ({sum(1 for r in missing if r['oa_status']=='closed')} closed, "
          f"{sum(1 for r in missing if r['oa_status']!='closed')} oa_but_blocked)")
    print(f"-> {LOG.relative_to(ROOT)} ; {MISSING.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
