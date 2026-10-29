"""Pomelo signup demo: static frontend plus a mock API."""

import json
import logging
import mimetypes
import os
import re
import threading
import traceback
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from alerts import send_alert
from insurance.eligibility import verify_eligibility

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
REPO = "github.com/sophialyssy-demo/pomelo-signup-demo"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("signup-api")


def mask(s, keep=2):
    s = str(s or "")
    return s[:keep] + "*" * max(0, len(s) - keep)


def otp_send(body):
    log.info("otp.send phone=%s (mock, no SMS sent)", mask(body.get("phone"), 3))
    return 200, {"sent": True}


def otp_verify(body):
    ok = bool(re.fullmatch(r"\d{6}", str(body.get("code", ""))))
    return (200, {"verified": True}) if ok else (400, {"error": "invalid_code"})


def membership_lookup(body):
    missing = [k for k in ("first", "last", "dob", "email") if not body.get(k)]
    if missing:
        return 400, {"error": "missing_fields", "fields": missing}
    return 200, {"member_id": "PMC-" + uuid.uuid4().hex[:8].upper(), "status": "pending_insurance"}


def insurance_connect(body):
    member = dict(body.get("member") or {}, group=body.get("group"))
    result = verify_eligibility(body.get("payer"), body.get("memberId"), member)
    return 200, {"eligible": result.eligible, "plan": result.plan_name, "payer": result.payer_name}


ROUTES = {
    "/api/otp/send": otp_send,
    "/api/otp/verify": otp_verify,
    "/api/membership/lookup": membership_lookup,
    "/api/insurance/connect": insurance_connect,
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log.info("%s %s", self.address_string(), fmt % args)

    def _send(self, status, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/healthz":
            return self._send(200, {"ok": True})
        if path.startswith("/static/"):
            f = (STATIC / path[len("/static/"):]).resolve()
            if STATIC.resolve() in f.parents and f.is_file():
                return self._send(200, f.read_bytes(), mimetypes.guess_type(f.name)[0] or "application/octet-stream")
            return self._send(404, {"error": "not_found"})
        return self._send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        handler = ROUTES.get(path)
        if handler is None:
            return self._send(404, {"error": "not_found"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            status, resp = handler(body)
            return self._send(status, resp)
        except Exception as exc:
            ref = "ERR-" + uuid.uuid4().hex[:10].upper()
            tb = traceback.format_exc()
            log.error("unhandled error ref=%s path=%s\n%s", ref, path, tb)
            event = {
                "title": f"500 on POST {path}: {type(exc).__name__}: {exc}",
                "fingerprint": f"{path}:{type(exc).__name__}:{exc}",
                "severity": "high",
                "service": "pomelo-signup-api",
                "environment": os.environ.get("APP_ENV", "demo"),
                "endpoint": f"POST {path}",
                "error_ref": ref,
                "exception": {"type": type(exc).__name__, "message": str(exc), "traceback": tb},
                "context": {
                    "user_step": "Connect your insurance" if "insurance" in path else path,
                    "payer": body.get("payer") if isinstance(body, dict) else None,
                    "member_id": mask(body.get("memberId")) if isinstance(body, dict) else None,
                },
                "repo": REPO,
                "occurred_at": datetime.now(timezone.utc).isoformat(),
            }
            threading.Thread(target=send_alert, args=(event,), daemon=True).start()
            return self._send(500, {"error": "internal_error", "error_ref": ref})


def main():
    port = int(os.environ.get("PORT", "8080"))
    log.info("Pomelo signup demo on http://localhost:%s/signup/reason-for-care", port)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
