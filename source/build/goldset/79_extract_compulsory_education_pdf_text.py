#!/usr/bin/env python3
"""Extract validated compulsory-education PDFs to text for auditable full-text review."""

import csv
import re
from pathlib import Path

from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RETRIEVAL = REPO / "output/compulsory-education-pdf-retrieval-manifest.csv"
TEXT_DIR = REPO / "temp/compulsory-education-fulltext"
MANIFEST = REPO / "output/compulsory-education-fulltext-text-manifest.csv"

FIELDS = ["paperId", "doi", "title", "pdf_path", "text_path", "pages", "characters", "status", "reason"]


def clean(text):
    text = re.sub(r"-\n(?=\w)", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    with RETRIEVAL.open(newline="", encoding="utf-8-sig") as handle:
        sources = list(csv.DictReader(handle))
    output = []
    for row in sources:
        if row["status"] != "RETRIEVED":
            continue
        pdf_path = REPO / row["pdf_path"]
        text_path = TEXT_DIR / f"{row['paperId']}.txt"
        if text_path.exists() and text_path.stat().st_size >= 1000:
            text = text_path.read_text(encoding="utf-8")
            output.append({
                "paperId": row["paperId"], "doi": row["doi"], "title": row["title"],
                "pdf_path": row["pdf_path"], "text_path": str(text_path.relative_to(REPO)),
                "pages": "", "characters": len(text), "status": "OK", "reason": "cached extracted text",
            })
            continue
        try:
            document = PdfReader(str(pdf_path))
            pages = len(document.pages)
            text = clean("\n".join((page.extract_text() or "") for page in document.pages))
            if len(text) < 1000:
                status, reason = "TEXT_TOO_SHORT", "scanned, protected, or non-extractable PDF"
            else:
                text_path.write_text(text, encoding="utf-8")
                status, reason = "OK", ""
        except Exception as error:
            pages, text = 0, ""
            status, reason = "EXTRACTION_ERROR", str(error)
        output.append({
            "paperId": row["paperId"], "doi": row["doi"], "title": row["title"],
            "pdf_path": row["pdf_path"],
            "text_path": str(text_path.relative_to(REPO)) if status == "OK" else "",
            "pages": pages, "characters": len(text), "status": status, "reason": reason,
        })
    with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(f"text extracted: {sum(row['status'] == 'OK' for row in output)}/{len(output)} retrieved PDFs")
    for row in output:
        print(f"{row['status']:16s} {row['pages']:3} pages {row['characters']:8} chars  {row['title'][:60]}")


if __name__ == "__main__":
    main()
