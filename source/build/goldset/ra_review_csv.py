import csv
import json
from pathlib import Path


FIELDNAMES = [
    "Rank",
    "Score (0-10)",
    "Title",
    "Authors",
    "Journal",
    "Year",
    "DOI",
    "Confidence",
    "Score Rationale (AI)",
    "Screen Reason (AI)",
    "RA Decision",
    "RA Notes",
]

AUDIT_EXTRA_FIELDNAMES = [
    "Paper ID",
    "DOI Trust",
    "DOI Flag",
    "WID Status",
    "Score Source",
    "Recommended Disposition",
]


def norm_doi(value):
    if not value:
        return ""
    value = str(value).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    return value


def norm_title(value):
    return " ".join(str(value or "").lower().split())


def authors_to_text(value):
    if isinstance(value, list):
        return "; ".join(str(v) for v in value if v)
    return str(value or "")


def is_doi_trusted(record):
    return bool(norm_doi(record.get("doi_final") or record.get("doi"))) and record.get("doi_trust") != "UNRESOLVED"


def split_ra_review_records(records):
    review = []
    audit = []
    for record in records:
        if is_doi_trusted(record):
            review.append(record)
        else:
            audit.append(record)
    return review, audit


def load_json(path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def build_lookup(records, key):
    out = {}
    for record in records:
        value = record.get(key)
        if value:
            out.setdefault(value, record)
    return out


def build_title_lookup(records):
    out = {}
    for record in records:
        title = norm_title(record.get("title"))
        if title:
            out.setdefault(title, record)
    return out


def build_journal_lookups(canon_records):
    journal_by_doi = {}
    journal_by_title = {}
    for record in canon_records:
        venue = record.get("venue") or ""
        if not venue:
            continue
        doi = norm_doi(record.get("final_doi") or record.get("doi"))
        title = norm_title(record.get("title"))
        if doi:
            journal_by_doi[doi] = venue
        if title:
            journal_by_title[title] = venue
    return journal_by_doi, journal_by_title


def make_row(rank, record, candidate, screen, journal_by_doi, journal_by_title):
    title_key = norm_title(record.get("title"))
    doi = norm_doi(record.get("doi_final") or record.get("doi"))
    return {
        "Rank": rank,
        "Score (0-10)": record.get("compositeScore", ""),
        "Title": record.get("title", ""),
        "Authors": authors_to_text(record.get("authors")),
        "Journal": journal_by_doi.get(doi) or journal_by_title.get(title_key) or "",
        "Year": record.get("year", ""),
        "DOI": doi,
        "Confidence": candidate.get("confidence") or screen.get("llm_confidence") or "",
        "Score Rationale (AI)": record.get("scoreRationale") or record.get("mechanism") or "",
        "Screen Reason (AI)": screen.get("llm_reason") or "",
        "RA Decision": "",
        "RA Notes": "",
    }


def write_csv(path, fieldnames, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_ra_review_csvs(logs_dir, output_dir, slug):
    logs_dir = Path(logs_dir)
    output_dir = Path(output_dir)

    studies_path = logs_dir / f"{slug}-metaanalysis-studies.json"
    if studies_path.exists():
        final_records = load_json(studies_path)
        source_file = studies_path.name
    else:
        final_records = load_json(logs_dir / f"{slug}-metaanalysis-ready-final.json")
        source_file = f"{slug}-metaanalysis-ready-final.json"
    candidates = load_json(logs_dir / f"{slug}-metaanalysis-candidates.json")
    prioritized = load_json(logs_dir / f"{slug}-prioritized.json")["papers"]
    sequential = load_json(logs_dir / f"{slug}-sequential-screened.json")["papers"]
    canon = load_json(logs_dir / f"{slug}-canon-resolved.json")

    candidate_by_id = build_lookup(candidates, "paperId")
    candidate_by_title = build_title_lookup(candidates)

    screen_by_id = {}
    screen_by_title = {}
    for source in (prioritized, sequential):
        screen_by_id.update({k: v for k, v in build_lookup(source, "paperId").items() if k not in screen_by_id})
        screen_by_title.update({k: v for k, v in build_title_lookup(source).items() if k not in screen_by_title})

    journal_by_doi, journal_by_title = build_journal_lookups(canon)
    review_records, audit_records = split_ra_review_records(final_records)

    review_rows = []
    audit_rows = []
    for rank, record in enumerate(final_records, start=1):
        paper_id = record.get("paperId")
        title_key = norm_title(record.get("title"))
        candidate = candidate_by_id.get(paper_id) or candidate_by_title.get(title_key) or {}
        screen = screen_by_id.get(paper_id) or screen_by_title.get(title_key) or {}
        row = make_row(rank, record, candidate, screen, journal_by_doi, journal_by_title)
        if record in review_records:
            review_rows.append(row)
        else:
            audit_rows.append({
                **row,
                "Paper ID": paper_id or "",
                "DOI Trust": record.get("doi_trust") or "",
                "DOI Flag": record.get("doi_flag") or "",
                "WID Status": record.get("wid_status") or "",
                "Score Source": record.get("score_source") or "",
                "Recommended Disposition": "HOLD OUT until independently verified",
            })

    review_path = output_dir / f"{slug}-ra-review.csv"
    audit_path = output_dir / f"{slug}-unresolved-audit.csv"
    write_csv(review_path, FIELDNAMES, review_rows)
    write_csv(audit_path, FIELDNAMES + AUDIT_EXTRA_FIELDNAMES, audit_rows)

    return {
        "review_path": str(review_path),
        "audit_path": str(audit_path),
        "total": len(final_records),
        "review": len(review_rows),
        "audit": len(audit_rows),
        "source_file": source_file,
    }
