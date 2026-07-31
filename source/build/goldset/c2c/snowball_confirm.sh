#!/bin/bash
# Channel-3 snowball, CONFIRMING ROUND for C.2.c (round 4).
#
# WHY THIS DESIGN. Rounds 1-3 each added seeds that *I* picked to reach an under-covered sub-area.
# That makes the marginal-yield measurement a test of RA imagination, not of exhaustion -- the §7.2
# defect written up in the log. A literal same-seed re-run is useless: backward refs and forward
# citations of a fixed seed are deterministic, so it returns zero by construction and proves nothing.
#
# The confirming round therefore keeps the *rule* of "no new hand-picked seeds" while making the
# frontier expansion MECHANICAL: seed from EVERY paper already in the Tier-B frame that has not
# already been used as a seed. Selection is by membership, not judgement. If the citation
# neighbourhood is genuinely exhausted, a mechanical sweep of the whole frontier returns few new
# relevant papers per record pulled; if it is not, this finds what RA judgement missed.
#
# This is the only version of the stop test that measures the thing §7.2 means to measure.
set -u
M="shravanh@uchicago.edu"
OUT="${1:?usage: snowball_confirm.sh <outdir>}"
FRAME="literature/search-logs/housing-costs-tier-b-frame.json"
mkdir -p "$OUT"

# Seeds already used in rounds 1-3 (including preprint twins) -- excluded from the confirming sweep.
USED="W3024244835 W2017790450 W3037455063 W3131143603 W2037422701 W2035671284 W1578574739
W2125780906 W2065377959 W1509700920 W2131771089 W2532821622 W2099386106 W2129646919
W4395481274 W3217487213 W4392854776 W1693336056 W3028664058 W4399107829 W2086486830 W2132599910"

python3 - "$FRAME" "$OUT" "$USED" <<'PY'
import json, sys
frame, out, used = sys.argv[1], sys.argv[2], set(sys.argv[3].split())
ids = [r["openalex"] for r in json.load(open(frame)) if r["openalex"] not in used]
open(out + "/seed_ids.txt", "w").write("\n".join(ids))
print(f"confirming-round seeds: {len(ids)} (mechanical: every Tier-B frame member not already a seed)")
PY

echo "== backward refs =="
: > "$OUT/backrefs_all.txt"
n=0
while read -r wid; do
  curl -s --max-time 40 "https://api.openalex.org/works/$wid?mailto=$M" \
    | python3 -c "
import json,sys
try: w=json.load(sys.stdin)
except Exception: sys.exit()
for r in (w.get('referenced_works') or []): print(r.rsplit('/',1)[-1])
" >> "$OUT/backrefs_all.txt"
  n=$((n+1)); [ $((n % 25)) -eq 0 ] && echo "  ...$n seeds"
done < "$OUT/seed_ids.txt"
echo "  backward refs collected: $(wc -l < "$OUT/backrefs_all.txt")"

echo "== forward citations =="
: > "$OUT/fwd_all.jsonl"
n=0
while read -r wid; do
  page=1
  while : ; do
    resp=$(curl -s --max-time 60 -G "https://api.openalex.org/works" \
      --data-urlencode "filter=cites:$wid" --data-urlencode "per-page=200" \
      --data-urlencode "page=$page" --data-urlencode "mailto=$M" \
      --data-urlencode "select=id,doi,title,publication_year,type,cited_by_count,primary_location")
    cnt=$(printf '%s' "$resp" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('results',[])))" 2>/dev/null || echo 0)
    printf '%s\n' "$resp" >> "$OUT/fwd_all.jsonl"
    [ "$cnt" -lt 200 ] && break
    page=$((page+1)); [ "$page" -gt 3 ] && break
  done
  n=$((n+1)); [ $((n % 25)) -eq 0 ] && echo "  ...$n seeds"
done < "$OUT/seed_ids.txt"
echo "confirming round pull complete"
