# Webhooks

Soz Ledger supports webhook notifications that allow your application to receive real-time updates when events occur in the trust network. Instead of polling the API, you can register a webhook URL and receive HTTP POST requests whenever relevant events happen.

## Event Types

Soz Ledger emits the following webhook event types:

| Event Type | Trigger |
|------------|---------|
| `promise.created` | A new promise has been created where you are the promisor or promisee. |
| `promise.fulfilled` | A promise you are party to has been marked as fulfilled. |
| `promise.broken` | A promise you are party to has been marked as broken. |
| `promise.expired` | A promise you are party to has expired (deadline passed without resolution). |
| `score.updated` | Your entity's trust score has been recomputed. |
| `evidence.submitted` | New evidence has been submitted for a promise you are party to. |

## Payload Structure

All webhook payloads follow a consistent envelope structure:

```json
{
  "event_type": "string",
  "event_id": "string (UUID)",
  "timestamp": "string (ISO 8601)",
  "data": { }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `event_type` | string | The type of event (see table above). |
| `event_id` | string (UUID) | A unique identifier for this event delivery. Can be used for idempotency. |
| `timestamp` | string (ISO 8601) | When the event occurred, in UTC. |
| `data` | object | The event-specific payload. Structure varies by event type. |

## Event Payloads

### promise.created

Fired when a new promise is created involving your entity.

```json
{
  "event_type": "promise.created",
  "event_id": "e1a2b3c4-d5e6-7890-abcd-ef1234567890",
  "timestamp": "2026-02-10T12:30:00Z",
  "data": {
    "promise": {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "promisor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
      "description": "Deliver processed dataset with sentiment analysis results",
      "category": "delivery",
      "status": "active",
      "deadline": "2026-02-15T18:00:00Z",
      "created_at": "2026-02-10T12:30:00Z"
    }
  }
}
```

### promise.fulfilled

Fired when a promise is marked as fulfilled.

```json
{
  "event_type": "promise.fulfilled",
  "event_id": "f2b3c4d5-e6f7-8901-bcde-f23456789012",
  "timestamp": "2026-02-14T09:15:00Z",
  "data": {
    "promise": {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "promisor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
      "description": "Deliver processed dataset with sentiment analysis results",
      "category": "delivery",
      "status": "fulfilled",
      "deadline": "2026-02-15T18:00:00Z",
      "fulfilled_at": "2026-02-14T09:15:00Z",
      "created_at": "2026-02-10T12:30:00Z"
    }
  }
}
```

### promise.broken

Fired when a promise is marked as broken.

```json
{
  "event_type": "promise.broken",
  "event_id": "a3c4d5e6-f7a8-9012-cdef-345678901234",
  "timestamp": "2026-02-16T00:00:00Z",
  "data": {
    "promise": {
      "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "promisor_id": "d34ef012-34ab-5678-90cd-ef1234567890",
      "promisee_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "description": "Complete API integration for payment processing module",
      "category": "delivery",
      "status": "broken",
      "deadline": "2026-02-15T23:59:59Z",
      "broken_at": "2026-02-16T00:00:00Z",
      "created_at": "2026-02-08T10:00:00Z"
    }
  }
}
```

### promise.expired

Fired when a promise's deadline passes without the promise being fulfilled or explicitly broken.

```json
{
  "event_type": "promise.expired",
  "event_id": "b4d5e6f7-a8b9-0123-def0-456789012345",
  "timestamp": "2026-02-15T18:00:01Z",
  "data": {
    "promise": {
      "id": "c3d4e5f6-a7b8-9012-cdef-678901234567",
      "promisor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "promisee_id": "e45f0123-45bc-6789-01de-f23456789012",
      "description": "Respond to partnership inquiry with pricing proposal",
      "category": "response",
      "status": "expired",
      "deadline": "2026-02-15T18:00:00Z",
      "created_at": "2026-02-12T14:00:00Z"
    }
  }
}
```

### score.updated

Fired when an entity's trust score is recomputed (typically after a promise outcome is recorded).

```json
{
  "event_type": "score.updated",
  "event_id": "c5e6f7a8-b9c0-1234-ef01-567890123456",
  "timestamp": "2026-02-14T09:15:05Z",
  "data": {
    "entity_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "previous_score": 0.83,
    "new_score": 0.85,
    "previous_level": "Highly Trusted",
    "new_level": "Highly Trusted",
    "is_rated": true,
    "total_promises": 47,
    "fulfilled_count": 40,
    "broken_count": 3
  }
}
```

### evidence.submitted

Fired when new evidence is submitted for a promise you are party to.

```json
{
  "event_type": "evidence.submitted",
  "event_id": "d6f7a8b9-c0d1-2345-f012-678901234567",
  "timestamp": "2026-02-14T09:14:00Z",
  "data": {
    "evidence": {
      "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "promise_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "submitted_by": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "evidence_type": "link",
      "content": "https://storage.example.com/datasets/sentiment-results-20260214.csv",
      "metadata": {
        "file_size": "2.3MB",
        "row_count": 15000
      },
      "created_at": "2026-02-14T09:14:00Z"
    },
    "promise_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }
}
```

## Delivery Details

### HTTP Method and Format

Webhooks are delivered as **HTTP POST** requests with a `Content-Type: application/json` header. The request body is the JSON payload described above.

### Headers

Each webhook delivery includes the following headers:

| Header | Description |
|--------|-------------|
| `Content-Type` | Always `application/json`. |
| `X-SozLedger-Event` | The event type (e.g., `promise.fulfilled`). |
| `X-SozLedger-Delivery-Id` | The unique event ID, matching `event_id` in the payload. |
| `X-SozLedger-Timestamp` | The event timestamp in ISO 8601 format. |
| `X-SozLedger-Signature` | HMAC-SHA256 signature of the payload for verification (see Verifying Signatures). |

### Expected Response

Your webhook endpoint should return a `2xx` HTTP status code to acknowledge receipt. Any non-`2xx` response (or a timeout) will be treated as a delivery failure.

### Retry Policy

If a webhook delivery fails, Soz Ledger will retry with exponential backoff:

| Attempt | Delay |
|---------|-------|
| 1st retry | 1 minute |
| 2nd retry | 5 minutes |
| 3rd retry | 30 minutes |
| 4th retry | 2 hours |
| 5th retry | 12 hours |

After 5 failed retries, the delivery is marked as failed and will not be retried further. Failed deliveries can be reviewed through the webhook management interface.

## Verifying Signatures

To ensure that a webhook delivery is genuinely from Soz Ledger and has not been tampered with, verify the `X-SozLedger-Signature` header.

### Verification Steps

1. Retrieve the raw request body (before any parsing).
2. Compute an HMAC-SHA256 hash of the raw body using your webhook signing secret.
3. Compare the computed hash with the value in `X-SozLedger-Signature`.

### Example (Python)

```python
import hmac
import hashlib

def verify_webhook(payload_body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode("utf-8"),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### Example (Node.js)

```javascript
const crypto = require("crypto");

function verifyWebhook(payloadBody, signature, secret) {
  const expected = crypto
    .createHmac("sha256", secret)
    .update(payloadBody)
    .digest("hex");
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signature)
  );
}
```

## Webhook Registration

Webhook registration is planned for a future API release. The registration endpoint will allow you to:

- **Register a webhook URL** for your entity.
- **Select event types** to subscribe to (or subscribe to all events).
- **Retrieve your webhook configuration** and delivery history.
- **Update or delete** webhook registrations.
- **Rotate signing secrets** for webhook verification.

### Planned Registration API

```
POST   /v1/webhooks          - Register a new webhook endpoint
GET    /v1/webhooks           - List your webhook registrations
GET    /v1/webhooks/:id       - Get a specific webhook registration
PATCH  /v1/webhooks/:id       - Update a webhook registration
DELETE /v1/webhooks/:id       - Remove a webhook registration
GET    /v1/webhooks/:id/logs  - View delivery logs for a webhook
```

Until the registration API is available, webhook configuration can be arranged by contacting the Soz Ledger team.

## Best Practices

1. **Respond quickly.** Return a `200 OK` as soon as you receive the webhook, then process the event asynchronously. Long-running processing in the webhook handler can cause timeouts.

2. **Handle duplicates.** Use the `event_id` field to implement idempotency. In rare cases (network issues, retries), the same event may be delivered more than once.

3. **Verify signatures.** Always verify the `X-SozLedger-Signature` header before trusting the payload content.

4. **Use HTTPS.** Your webhook endpoint must be served over HTTPS. HTTP endpoints will not receive deliveries.

5. **Monitor failures.** Set up alerting for webhook delivery failures so you can investigate connectivity issues promptly.

6. **Process events in order.** While Soz Ledger delivers events in chronological order under normal conditions, network retries can cause out-of-order delivery. Use the `timestamp` field to determine event ordering if needed.
