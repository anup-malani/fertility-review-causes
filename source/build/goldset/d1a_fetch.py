#!/usr/bin/env python3
"""
d1a_fetch.py — the ONE cached JSON fetcher for the D.1.a snowball scripts.

EXTRACTED BECAUSE THE COPY IN 93 HAD A BUG THAT SILENTLY ZEROED A SEED, AND 96 INHERITED IT VERBATIM.

Semantic Scholar answers an unauthenticated throttle with

    {"message": "Too Many Requests. Please wait and try again or apply for a key for higher rate
     limits. https://www.semanticscholar.org/product/api#api-key-form", "code": "429"}

and the guard was `d.get("message") == "Too Many Requests"` -- an equality test against a prefix of the
real message. It never fired. The 429 body therefore passed the "looks like JSON, has no `error` key"
check, was CACHED AS A SUCCESSFUL RESPONSE, and the caller read `d.get("data") or []` off it and
recorded an empty list. The seed came back `status=OK, n=0`.

That is the worst available failure mode and it is the one this chapter keeps meeting: a throttled
request reported as a completed pull of zero records. It is the same shape as the OpenAlex
five-operator throttle from the channel-1 probe ("a throttled query that still returns a plausible
count is the failure mode that does not announce itself") and the same shape as the relevance filter
that was wrong in both directions. It surfaced here only because the first seed it hit was van de Kaa
1987, whose true neighbourhood is ~1,300 citations, so `n=0` was obviously wrong. On any of the 84
generation-2 seeds it would have looked entirely normal.

Round 1's stored numbers are NOT affected -- the cache was audited entry by entry and the only two
poisoned records were written by the round-2 run that caught this. But round 1 was lucky rather than
safe: it hit the throttle on cells that failed in a way that DID return None, which is why they came
out as UNCONFIRMED rather than as zeroes.

THE THREE-STATE DISCIPLINE ONLY WORKS IF THE TRANSPORT LAYER RESPECTS IT. UNCONFIRMED means the
provider did not answer and is a statement about the network; a zero means the provider answered and
there is nothing there, a statement about the literature. A cached 429 converts the first into the
second, which is exactly the direction that manufactures false absences.
"""
import json, os, subprocess, time

# Body markers are the FALLBACK path only, for providers that answer HTTP 200 with an error payload
# (OpenAlex does this for budget exhaustion). The primary signal is the HTTP status code.
#
# NOTE WHAT IS NOT IN THIS LIST AND WHY. A bare "429" was, and it matched the substring 429 inside the
# Unix timestamp 1429894924000 in a perfectly good Crossref record for Inglehart 1977. Valid responses
# were therefore classified as throttles, retried six times, and recorded as UNCONFIRMED -- the very
# failure this module was written to eliminate, reintroduced by the fix for it.
#
# It is the same defect as `hous` matching hOUSEhold in the C.2.c filter and `reproduc\w+` matching
# social reproduction in this chapter's v1 filter: an unanchored substring test run against text that
# was never meant to be searched. Third occurrence in this codebase, first one inside the transport
# layer rather than a relevance filter, which is why it produced a network-shaped symptom and took a
# packet capture rather than a hand read to find. The lesson generalises past regexes: match on the
# field that carries the meaning (the status code), not on a string that happens to contain it.
THROTTLE_MARKERS = ("too many requests", "rate limit", "insufficient budget", "quota exceeded",
                    "slow down")


def is_not_found(d):
    """True if the provider ANSWERED and said it has no such record.

    A THIRD STATE, and it is not a nicety. Semantic Scholar answers an unknown identifier with
    `{"error":"Paper with id DOI:10.1016/b978-0-444-53187-2.00011-5 not found"}`, which has no `data`
    key, so a caller reading `d.get("data") or []` records ZERO CITATIONS for a work that S2 simply
    does not index. That is a false statement about the literature dressed as a measurement of it:
    Fernandez's *Does Culture Matter?* is the economics-of-culture family's only seed, and the
    difference between "this family has no citing literature" and "this seed is not in this index"
    is the difference between a finding and an artifact.

    Distinct from a throttle, which is retried, and distinct from a genuine zero, which is a fact
    about the record. Not retried -- the provider gave a definitive answer -- and safe to cache.
    """
    if not isinstance(d, dict):
        return False
    return "not found" in _scalar_fields(d) and not is_throttle(d)


def _scalar_fields(d):
    """Only TOP-LEVEL STRING fields. Crossref puts the entire work record under `message`, so
    stringifying it drags timestamps, ISBNs and page ranges into a text search that was meant to read
    a short error sentence. An error message is a string; a payload is not."""
    return " ".join(v for k, v in d.items()
                    if k in ("message", "error", "detail", "Error") and isinstance(v, str)).lower()


def is_throttle(d):
    """True if this JSON body is a provider refusing to answer, in any of its several dialects."""
    if not isinstance(d, dict):
        return False
    if str(d.get("code")) in ("429", "503"):
        return True
    return any(m in _scalar_fields(d) for m in THROTTLE_MARKERS)


class Fetcher:
    """Cached GET returning parsed JSON, or None meaning UNCONFIRMED -- the provider did not answer.

    A throttle is retried with exponential backoff and, if it never clears, returned as None. It is
    never cached: caching a refusal makes it permanent, and every later run inherits a false zero.
    """

    # PACE FIRST, BACK OFF SECOND. Reactive backoff alone does not work against an unauthenticated
    # Semantic Scholar limit and the round-2 run demonstrated it: once S2 starts refusing, every
    # subsequent request refuses too, so each one burns the full retry ladder (~113s) before
    # returning None. The run reached generation-2 seed 6 of 82 in seven minutes and would have
    # recorded most of the rest as UNCONFIRMED -- converting a rate limit into missing literature.
    # A minimum interval between requests to the same host keeps us under the limit instead of
    # discovering it, which is both faster in wall-clock and honest in the output.
    MIN_INTERVAL = {"api.semanticscholar.org": 3.5, "api.crossref.org": 0.2}

    def __init__(self, cache_path, ua, tries=6, base_sleep=1.2):
        self.path, self.ua, self.tries, self.base = cache_path, ua, tries, base_sleep
        self.cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
        self.throttled = 0   # counted and reported, so a slow run is visibly a slow run
        self._last = {}      # host -> monotonic time of the last request actually sent

    def _pace(self, url):
        host = url.split("/")[2] if "//" in url else ""
        gap = self.MIN_INTERVAL.get(host, 0.0)
        if not gap:
            return
        wait = gap - (time.monotonic() - self._last.get(host, 0.0))
        if wait > 0:
            time.sleep(wait)
        self._last[host] = time.monotonic()

    def purge_throttled(self):
        """Drop any cached body that is actually a provider refusal. Returns how many were removed."""
        bad = [k for k, v in self.cache.items() if is_throttle(v)]
        for k in bad:
            del self.cache[k]
        return len(bad)

    def save(self):
        json.dump(self.cache, open(self.path, "w"))

    def get(self, url, sleep=None):
        key = f"g::{url}"
        if key in self.cache:
            return self.cache[key]
        sleep = sleep or self.base
        for a in range(self.tries):
            self._pace(url)
            # THE STATUS CODE IS THE PRIMARY SIGNAL. Body sniffing is a fallback for providers that
            # answer 200 with an error payload, and it was body sniffing alone that produced both of
            # this module's own bugs. It also cannot see Crossref's 404, which is `text/plain`
            # "Resource not found." -- not JSON at all, so the old code retried it and reported
            # UNCONFIRMED for a DOI Crossref definitively does not hold.
            out = subprocess.run(["curl", "-s", "-m", "50", "-A", self.ua,
                                  "-w", "\n%{http_code}", url], capture_output=True, text=True)
            body, _, code = out.stdout.rpartition("\n")
            code = code.strip()
            if out.returncode != 0:
                time.sleep(sleep * (a + 2)); continue
            if code in ("429", "503", "504"):
                self.throttled += 1
                time.sleep(min(sleep * (2 ** a), 20.0))   # capped: pacing is the primary defence
                continue
            if code in ("404", "410"):
                self.cache[key] = {"error": "not found", "__http__": int(code)}
                return self.cache[key]
            if not body.strip().startswith("{"):
                time.sleep(sleep * (a + 2)); continue
            try:
                d = json.loads(body)
            except Exception:  # noqa: BLE001
                time.sleep(sleep * (a + 2)); continue
            if is_throttle(d):
                self.throttled += 1
                time.sleep(min(sleep * (2 ** a), 20.0))
                continue
            self.cache[key] = d
            return d
        return None
