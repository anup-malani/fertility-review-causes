import unittest
import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ra_review_csv import build_ra_review_csvs, split_ra_review_records


class RaReviewCsvTests(unittest.TestCase):
    def test_unresolved_doi_trust_is_excluded_from_ra_review(self):
        records = [
            {"paperId": "ok", "title": "Verified paper", "doi_final": "10.1/ok", "doi_trust": "openalex-fresh(guarded)"},
            {"paperId": "bad", "title": "Unresolved paper", "doi_final": None, "doi_trust": "UNRESOLVED"},
            {"paperId": "drift", "title": "Drift paper", "doi_final": "10.1/wrong", "doi_trust": "UNRESOLVED", "doi_flag": "WID_DRIFT"},
        ]

        review, audit = split_ra_review_records(records)

        self.assertEqual([r["paperId"] for r in review], ["ok"])
        self.assertEqual([r["paperId"] for r in audit], ["bad", "drift"])

    def test_ra_review_uses_distinct_study_file_when_available(self):
        slug = "sample"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs = root / "logs"
            out = root / "out"
            logs.mkdir()
            ready_final = [
                {"paperId": "published", "title": "Published Study", "doi_final": "10.1/published", "doi_trust": "gold-RA-verified", "authors": ["A"], "compositeScore": 10},
                {"paperId": "ssrn-version", "title": "Published Study Working Paper", "doi_final": "10.1/ssrn", "doi_trust": "openalex-fresh(guarded)", "authors": ["A"], "compositeScore": 10},
                {"paperId": "deposit", "title": "Data and Code for: Published Study", "doi_final": "10.3886/deposit", "doi_trust": "openalex-fresh(guarded)", "authors": ["A"], "compositeScore": 10},
            ]
            studies = [
                {"paperId": "published", "title": "Published Study", "doi_final": "10.1/published", "doi_trust": "gold-RA-verified", "authors": ["A"], "compositeScore": 10},
            ]
            fixtures = {
                f"{slug}-metaanalysis-ready-final.json": ready_final,
                f"{slug}-metaanalysis-studies.json": studies,
                f"{slug}-metaanalysis-candidates.json": [],
                f"{slug}-prioritized.json": {"papers": []},
                f"{slug}-sequential-screened.json": {"papers": []},
                f"{slug}-canon-resolved.json": [],
            }
            for name, value in fixtures.items():
                (logs / name).write_text(json.dumps(value), encoding="utf-8")

            result = build_ra_review_csvs(logs, out, slug)

            self.assertEqual(result["total"], 1)
            self.assertEqual(result["review"], 1)
            self.assertEqual(result["audit"], 0)


if __name__ == "__main__":
    unittest.main()
