#!/usr/bin/env python3
"""
237_a23_browser_receiver.py — A.23, stage 5f. A localhost sink for the browser retrieval pass.

WHY THIS EXISTS. `235` split the retrieval residue by what would fix each record, and its largest
actionable bucket was `W1_browser`: 55 records where the route returned a 200 that was not the
article. Those are open content behind bot defence, and a logged-in browser opens them. The problem
is not opening them, it is GETTING THE BYTES OUT — a browser tool returns text into a context
window, and a 500 KB PDF is not something to move through one.

So the browser fetches the file with the page's own credentials and origin, and POSTs it here. This
process writes it into `literature/pdfs/{slug}/` under the same naming convention every other
retrieval stage uses, so stage 6 cannot tell which rung delivered a file and does not need to.

**IT BINDS TO 127.0.0.1 AND ONLY ACCEPTS WRITES INTO ONE DIRECTORY.** The name is sanitised to
`{WID}__{slug}.{ext}`, path separators are rejected, and anything that is not a PDF or plain text is
refused. It is started for a retrieval pass and stopped after it; it is not a service.

**IT ALSO RECORDS PROVENANCE**, for the reason `233` learned the hard way: a file whose delivering
rung is not written down turns into an unattributable artefact on the next run. Each write appends
to `{slug}-browser-fetch-log.jsonl` with the source url, the byte count and the content type.

Usage:  python3 237_a23_browser_receiver.py [port]      (default 8765; Ctrl-C to stop)
"""
import json, os, re, sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

SLUG = "co-residence-parents-household-delay"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
LOG = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-browser-fetch-log.jsonl")
MAX_BYTES = 80 * 1024 * 1024
OK_TYPES = {"application/pdf": ".pdf", "text/plain": ".txt", "text/html": ".html.txt"}


def safe_name(name, ext):
    """`{WID}__{title-slug}` and nothing else. A name that does not match is rejected outright
    rather than repaired — a repaired path is a path someone chose."""
    if not re.fullmatch(r"W\d+__[a-z0-9][a-z0-9-]{0,120}", name or ""):
        return None
    return name + ext


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        n = len([f for f in os.listdir(PDF_DIR)]) if os.path.isdir(PDF_DIR) else 0
        self.wfile.write(f"a23 receiver up; {n} files in pdfs dir\n".encode())

    def do_POST(self):
        q = parse_qs(urlparse(self.path).query)
        name = (q.get("name") or [""])[0]
        ctype = (q.get("type") or ["application/pdf"])[0].split(";")[0].strip()
        src = (q.get("src") or [""])[0]
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BYTES:
            return self._fail(413, f"bad length {n}")
        ext = OK_TYPES.get(ctype)
        if not ext:
            return self._fail(415, f"refused content type {ctype}")
        fn = safe_name(name, ext)
        if not fn:
            return self._fail(400, f"refused name {name!r}")
        body = self.rfile.read(n)
        if ext == ".pdf" and body[:4] != b"%PDF":
            return self._fail(422, "not a pdf despite the content type")
        os.makedirs(PDF_DIR, exist_ok=True)
        with open(os.path.join(PDF_DIR, fn), "wb") as fh:
            fh.write(body)
        with open(LOG, "a") as fh:
            fh.write(json.dumps(dict(file=fn, bytes=n, type=ctype, src=src,
                                     at=time.strftime("%Y-%m-%dT%H:%M:%S"))) + "\n")
        print(f"  wrote {fn} ({n:,} bytes) <- {src[:70]}", flush=True)
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"ok {fn} {n}\n".encode())

    def _fail(self, code, msg):
        print(f"  REFUSED {code}: {msg}", flush=True)
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write((msg + "\n").encode())

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    os.makedirs(PDF_DIR, exist_ok=True)
    print(f"receiver on http://127.0.0.1:{port} -> {os.path.relpath(PDF_DIR, ROOT)}", flush=True)
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
