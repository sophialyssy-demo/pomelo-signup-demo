# Pomelo Care signup demo

Clickable recreation of the Pomelo Care signup flow (`app.pomelocare.com/signup`) for demos. Nothing is real: no SMS is sent and no insurer is contacted.

Flow: reason for care → phone number → verification code (any 6 digits) → membership lookup → connect your insurance → **error**.

The insurance step calls `POST /api/insurance/connect`, which currently fails with a 500. The server reports every unhandled error to the Devin on-call webhook (`alerts.py`), and Devin investigates and posts in Slack.

## Run

```bash
export DEVIN_WEBHOOK_URL=...        # Devin automation webhook URL (optional)
export DEVIN_WEBHOOK_SECRET=...     # sent as X-Webhook-Secret
python3 server.py                   # http://localhost:8080/signup/reason-for-care
python3 -m unittest discover -s tests -t .
```

`ALERT_COOLDOWN_SECONDS` (default 300) stops repeat alerts for the same error.
