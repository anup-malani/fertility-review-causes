#!/bin/bash
# CLEAN de-ghost -> re-grade -> rebuild -> merge/gate, RESUMING across small OpenAlex budget
# windows. Each step is cache-resumable; on budget exhaustion a step exits 3 and we wait for
# the next window and re-run it (cached probes are free, so it advances each window until done).
set -u
cd "$(dirname "$0")"
LOG="clean_rerun.log"
echo "=== clean re-run (resuming) started $(date -u '+%Y-%m-%d %H:%M UTC') ===" >> "$LOG"

budget_ready() {
  curl -s -m 20 -A "oas/1.0 (mailto:shravanh@uchicago.edu)" \
    "https://api.openalex.org/works?filter=title.search:fertility&per-page=1&mailto=shravanh@uchicago.edu" \
    | grep -q '"count"'
}

run_until_done() {   # $1 = script; loop across budget windows until it exits 0
  local script="$1" attempt=0
  while true; do
    attempt=$((attempt+1))
    until budget_ready; do echo "  [$script] budget dry at $(date -u '+%H:%M UTC'); sleep 120" >> "$LOG"; sleep 120; done
    echo "--- $script attempt $attempt at $(date -u '+%H:%M UTC') ---" >> "$LOG"
    python3 "$script" >> "$LOG" 2>&1
    local rc=$?
    echo "$script exit=$rc" >> "$LOG"
    if [ $rc -eq 0 ]; then return 0; fi
    if [ $rc -ne 3 ]; then echo "$script hard-failed (exit $rc); stopping." >> "$LOG"; return $rc; fi
    echo "  [$script] budget exhausted mid-run; waiting for next window" >> "$LOG"
    sleep 120
  done
}

run_until_done 44_deghost_gold.py       || exit $?
python3 45_regrade_deghosted.py         >> "$LOG" 2>&1; echo "45 exit=$?" >> "$LOG"   # on-disk, no API
run_until_done 46_rebuild_gold_enumerate.py || exit $?
python3 47_merge_refreeze_gate.py       >> "$LOG" 2>&1; echo "47 exit=$?" >> "$LOG"   # on-disk, no API

echo "=== clean re-run finished $(date -u '+%Y-%m-%d %H:%M UTC') ===" >> "$LOG"
echo "GATE DECISION:" >> "$LOG"
python3 -c "import json;d=json.load(open('../../../output/old-age-security-pension-crowdout-gate-decision.json'));print(json.dumps(d,indent=2))" >> "$LOG" 2>&1
