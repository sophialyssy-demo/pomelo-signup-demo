"""Sends production errors to the Devin on-call webhook."""

import json
import logging
import os
import threading
import time
import urllib.request

log = logging.getLogger("alerts")
_last_sent = {}
_lock = threading.Lock()


def send_alert(event):
    url = os.environ.get("DEVIN_WEBHOOK_URL")
    if not url:
        log.warning("DEVIN_WEBHOOK_URL not set; alert not sent: %s", event["title"])
        return False
    cooldown = int(os.environ.get("ALERT_COOLDOWN_SECONDS", "300"))
    key = event.get("fingerprint", event["title"])
    with _lock:
        if time.time() - _last_sent.get(key, 0) < cooldown:
            log.info("alert %s suppressed (cooldown)", key)
            return False
        _last_sent[key] = time.time()
    headers = {"Content-Type": "application/json"}
    secret = os.environ.get("DEVIN_WEBHOOK_SECRET")
    if secret:
        headers["X-Webhook-Secret"] = secret
    req = urllib.request.Request(url, data=json.dumps(event).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            log.info("alert sent: %s -> HTTP %s", event["title"], r.status)
            return True
    except Exception as e:  # alerting must never break the request path
        log.error("alert delivery failed: %s", e)
        return False
