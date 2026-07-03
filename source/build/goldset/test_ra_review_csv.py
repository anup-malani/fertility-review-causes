import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ra_review_csv import split_ra_review_records


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


if __name__ == "__main__":
    unittest.main()
