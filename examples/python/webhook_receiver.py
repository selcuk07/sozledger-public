"""
Soz Ledger -- Webhook Receiver Example
========================================
A minimal Flask application that receives webhook events from Soz Ledger
and routes them to handler functions.

Supported event types:
  - promise.created
  - promise.fulfilled
  - promise.broken
  - promise.disputed
  - evidence.submitted
  - score.updated

Run:
    pip install flask
    python webhook_receiver.py
"""

import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone

from flask import Flask, Response, abort, request

app = Flask(__name__)

# Replace with your webhook signing secret from the Soz Ledger dashboard.
WEBHOOK_SECRET = "your_webhook_secret"

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")
log = logging.getLogger("soz-webhooks")


# ── Signature verification ──────────────────────────────────────────────────
def verify_signature(payload_body: bytes, signature_header: str | None) -> bool:
    """
    Verify that the incoming request was actually sent by Soz Ledger.

    The signature is an HMAC-SHA256 hex digest of the raw request body,
    using your webhook secret as the key.  Soz Ledger sends it in the
    ``X-SozLedger-Signature`` header.
    """
    if signature_header is None:
        return False

    expected = hmac.new(
        key=WEBHOOK_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature_header)


# ── Event handlers ──────────────────────────────────────────────────────────
def handle_promise_created(data: dict) -> None:
    promise = data.get("promise", {})
    log.info(
        "Promise created: id=%s  promisor=%s  promisee=%s  category=%s",
        promise.get("id"),
        promise.get("promisor_id"),
        promise.get("promisee_id"),
        promise.get("category"),
    )


def handle_promise_fulfilled(data: dict) -> None:
    promise = data.get("promise", {})
    log.info(
        "Promise fulfilled: id=%s  fulfilled_at=%s",
        promise.get("id"),
        promise.get("fulfilled_at"),
    )


def handle_promise_broken(data: dict) -> None:
    promise = data.get("promise", {})
    log.info(
        "Promise broken: id=%s  promisor=%s",
        promise.get("id"),
        promise.get("promisor_id"),
    )


def handle_promise_disputed(data: dict) -> None:
    promise = data.get("promise", {})
    log.info(
        "Promise disputed: id=%s  promisor=%s",
        promise.get("id"),
        promise.get("promisor_id"),
    )


def handle_evidence_submitted(data: dict) -> None:
    evidence = data.get("evidence", {})
    log.info(
        "Evidence submitted: id=%s  promise=%s  type=%s  verified=%s",
        evidence.get("id"),
        evidence.get("promise_id"),
        evidence.get("type"),
        evidence.get("verified"),
    )


def handle_score_updated(data: dict) -> None:
    score = data.get("score", {})
    log.info(
        "Score updated: entity=%s  overall=%s  level=%s",
        score.get("entity_id"),
        score.get("overall_score"),
        score.get("level"),
    )


# Map event types to handler functions.
EVENT_HANDLERS = {
    "promise.created": handle_promise_created,
    "promise.fulfilled": handle_promise_fulfilled,
    "promise.broken": handle_promise_broken,
    "promise.disputed": handle_promise_disputed,
    "evidence.submitted": handle_evidence_submitted,
    "score.updated": handle_score_updated,
}


# ── Webhook endpoint ────────────────────────────────────────────────────────
@app.route("/webhooks", methods=["POST"])
def webhooks():
    # 1. Verify the request signature.
    signature = request.headers.get("X-SozLedger-Signature")
    if not verify_signature(request.get_data(), signature):
        log.warning("Invalid webhook signature -- rejecting request")
        abort(401)

    # 2. Parse the JSON body.
    try:
        event = request.get_json(force=True)
    except Exception:
        log.error("Malformed JSON in webhook body")
        abort(400)

    event_type = event.get("type", "unknown")
    log.info("Received webhook event: %s", event_type)

    # 3. Dispatch to the correct handler.
    handler = EVENT_HANDLERS.get(event_type)
    if handler:
        handler(event.get("data", {}))
    else:
        log.warning("Unhandled event type: %s", event_type)

    # 4. Always return 200 quickly so Soz Ledger does not retry.
    return Response(status=200)


if __name__ == "__main__":
    print("Starting Soz Ledger webhook receiver on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
