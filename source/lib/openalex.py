"""Shared OpenAlex client: pool fallback, throttle, refusal detection, and a measurement cache.

Written for TICK-079 because the machinery below was about to exist in two scripts, and this
repository already carries twelve divergent copies of the anchor resolver on `main` — a fix applied
to one copy is not applied to the literature. Everything here was measured on 2026-09-03; the
comments record what was measured, because every one of these behaviours reads as an empty
literature if it is not handled.

**Two different limits share one error string.** Both arrive as `{"error": "Rate limit exceeded"}`
and they need opposite responses:

  - `"Insufficient budget. ... you only have $0 remaining. Resets at midnight UTC"` — the client's
    DAILY BUDGET is spent. Retry tomorrow, not in a second. The budget is roughly 100 requests at
    $0.001 each, which one calibration pass can consume on its own.
  - `"Your query uses N boolean operators ... queries with more than 5 operators are limited to
    1 request per second per client"` — a THROTTLE on the keyless path. Retry after a second.

**The api_key is not a bypass and neither is going keyless.** The keyed path reported
`dailyRemainingUsd` 0.0004 while keyless requests still succeeded, which looks like "keyless is
free". It is not: 89 keyless requests later the keyless path reported 0. Same wallet. What keyless
*does* have is the extra boolean throttle, which the keyed path does not.

**A refusal is never a zero.** A refused query has no `meta.count`; returning 0 for it makes an
absence out of a budget error (`refusals-read-as-zeros`). Callers get an error, never a count.

**Measurements are cached to disk as they are bought.** With a ~100-request daily budget, an
interrupted run that keeps nothing wastes the whole allowance, and two stages cannot run on the same
day (`stage-output-must-survive-rerun`).
"""
import json
import subprocess
import time
from pathlib import Path

BASE = "https://api.openalex.org/works"
POLITE_MIN_INTERVAL = 1.15      # >5-boolean queries are 1/sec/client on the keyless path
_last_polite = [0.0]

POOL = {"key": 0, "polite": 0, "refused": 0, "throttle_waits": 0}


def budget_exhausted(body: str) -> bool:
    return "Insufficient budget" in body


def throttled(body: str) -> bool:
    return "boolean operators" in body


class OpenAlex:
    def __init__(self, key="", mailto="", cache_path=None):
        self.key, self.mailto = key, mailto
        self.cache_path = Path(cache_path) if cache_path else None
        self.cache = {}
        self.stats = {"hit": 0, "miss": 0}
        if self.cache_path and self.cache_path.exists():
            try:
                self.cache = json.loads(self.cache_path.read_text())
            except json.JSONDecodeError:
                self.cache = {}

    # ---------------------------------------------------------------- transport
    def _get(self, params, use_key, path=BASE):
        args = ["curl", "-sS", "--max-time", "120", "-G", path]
        for k, v in params.items():
            args += ["--data-urlencode", f"{k}={v}"]
        if use_key and self.key:
            args += ["--data-urlencode", f"api_key={self.key}"]
        else:
            gap = POLITE_MIN_INTERVAL - (time.monotonic() - _last_polite[0])
            if gap > 0:
                POOL["throttle_waits"] += 1
                time.sleep(gap)
            _last_polite[0] = time.monotonic()
        if self.mailto:
            args += ["--data-urlencode", f"mailto={self.mailto}"]
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            return None, f"curl rc={r.returncode}: {r.stderr.strip()[:160]}"
        try:
            return json.loads(r.stdout), None
        except json.JSONDecodeError:
            return None, f"non-JSON body (a syntax refusal, not an empty result): {r.stdout[:160]}"

    def get(self, params, path=BASE):
        """(json, error). `error` is set for ANY response without meta.count — never a silent 0."""
        d, err = self._get(params, use_key=True, path=path)
        if err is None and "meta" in d and d["meta"].get("count") is not None:
            POOL["key"] += 1
            return d, None
        body = "" if d is None else json.dumps(d)
        if budget_exhausted(body) or "Rate limit exceeded" in body:
            for attempt in range(4):
                d2, err2 = self._get(params, use_key=False, path=path)
                if err2 is None and "meta" in d2 and d2["meta"].get("count") is not None:
                    POOL["polite"] += 1
                    return d2, None
                b2 = "" if d2 is None else json.dumps(d2)
                if budget_exhausted(b2):
                    break                      # tomorrow, not in a second
                if not throttled(b2) and "Rate limit" not in b2:
                    break
                time.sleep(1.5 * (attempt + 1))
            d, err = d2, err2
        POOL["refused"] += 1
        if err:
            return None, err
        return None, f"query refused (NOT an empty literature): {json.dumps(d)[:220]}"

    # ---------------------------------------------------------------- cached count + id probe
    def _remember(self, key, value):
        self.cache[key] = value
        if self.cache_path:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(json.dumps(self.cache, indent=0, sort_keys=True) + "\n")

    def count(self, query):
        key = json.dumps(["count", query])
        if key in self.cache:
            self.stats["hit"] += 1
            return self.cache[key], None
        self.stats["miss"] += 1
        d, err = self.get({"filter": f"title_and_abstract.search:{query}", "per-page": "1"})
        if err:
            return None, err
        self._remember(key, d["meta"]["count"])
        return d["meta"]["count"], None

    def page_all(self, query, select, cap=None):
        """Every record for a query, by cursor. (records, error).

        Partial pages are cached as they arrive: at ~100 requests a day, a pull interrupted at page
        4 of 5 must not have to buy pages 1-3 again.
        """
        key = json.dumps(["pages", query, select])
        state = self.cache.get(key) or {"cursor": "*", "records": [], "done": False}
        if state["done"]:
            self.stats["hit"] += 1
            return state["records"], None
        while not state["done"]:
            self.stats["miss"] += 1
            d, err = self.get({"filter": f"title_and_abstract.search:{query}",
                               "per-page": "200", "cursor": state["cursor"], "select": select})
            if err:
                self._remember(key, state)     # keep what was already bought
                return state["records"], err
            state["records"].extend(d.get("results", []))
            nxt = (d.get("meta") or {}).get("next_cursor")
            state["cursor"] = nxt
            state["done"] = not nxt or not d.get("results") or (
                cap is not None and len(state["records"]) >= cap)
            self._remember(key, state)
        return state["records"], None
