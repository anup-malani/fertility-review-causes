#!/usr/bin/env python3
"""Format an OpenAlex works response piped in on stdin."""
import json
import sys

data = json.load(sys.stdin)
print(f"# total={data['meta']['count']}")
for w in data.get("results", []):
    doi = (w.get("doi") or "").replace("https://doi.org/", "") or "NO-DOI"
    title = (w.get("title") or "")[:100]
    venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    print(f"{w.get('publication_year')} c={w.get('cited_by_count'):<5} {(w.get('type') or '')[:11]:<11} "
          f"{doi:<38} {title} [{venue[:38]}]")
