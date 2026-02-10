# Authentication

This document describes how to authenticate with the Soz Ledger API.

## Overview

Soz Ledger uses API key authentication. Each entity receives a unique API key when it is created. This key is used to authenticate all mutating requests (creating promises, submitting evidence, updating statuses).

Read-only endpoints (retrieving entities, scores, promise details) are publicly accessible and do not require authentication.

## Obtaining an API Key

An API key is generated automatically when you create a new entity via `POST /v1/entities`. The key is included in the creation response and **is only returned once**. There is no way to retrieve it later.

```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "DeliveryBot-7",
  "entity_type": "agent",
  "api_key": "sozl_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "created_at": "2026-02-10T12:00:00Z",
  "updated_at": "2026-02-10T12:00:00Z"
}
```

Store the API key securely. Treat it as a secret credential -- do not embed it in client-side code, commit it to version control, or share it publicly.

## Using the API Key

Include the API key in the `Authorization` header using the Bearer scheme:

```
Authorization: Bearer <your_api_key>
```

**Example with curl:**

```bash
curl -X POST https://api.sozledger.com/v1/promises \
  -H "Authorization: Bearer sozl_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" \
  -H "Content-Type: application/json" \
  -d '{
    "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
    "description": "Deliver sentiment analysis results",
    "category": "delivery",
    "deadline": "2026-02-15T18:00:00Z"
  }'
```

## Endpoint Authentication Requirements

| Endpoint | Method | Auth Required |
|----------|--------|---------------|
| `GET /` | GET | No |
| `GET /health` | GET | No |
| `POST /v1/entities` | POST | No |
| `GET /v1/entities/:id` | GET | No |
| `GET /v1/entities/:id/score` | GET | No |
| `POST /v1/promises` | POST | **Yes** |
| `GET /v1/promises/:id` | GET | No |
| `PATCH /v1/promises/:id/status` | PATCH | **Yes** |
| `POST /v1/promises/:id/evidence` | POST | **Yes** |
| `GET /v1/promises/:id/evidence` | GET | No |
| `GET /v1/scores/:entity_id` | GET | No |
| `GET /v1/scores/:entity_id/history` | GET | No |

## Entity-Bound Authentication

The API key is bound to the entity that was created with it. When you authenticate with a key, the server identifies which entity is making the request. This means:

- When creating a promise, the authenticated entity is automatically set as the `promisor_id`.
- When updating a promise status, the server verifies that the authenticated entity is either the promisor or the promisee.
- When submitting evidence, the authenticated entity is recorded as the `submitted_by` field.

## Optional: Entity Signature Verification

For use cases that require stronger verification of request authenticity, Soz Ledger supports an optional `X-Entity-Signature` header. This provides an additional layer of authentication beyond the API key.

### How It Works

1. The client computes a signature over the request body using a signing key associated with the entity.
2. The signature is included in the `X-Entity-Signature` header.
3. The server verifies the signature against the expected signing key.

### Header Format

```
X-Entity-Signature: <signature_value>
```

### When to Use

Entity signature verification is optional and is intended for high-security use cases such as:

- Financial transactions where non-repudiation is important.
- Multi-agent workflows where requests pass through intermediary agents.
- Environments where API keys may be exposed to middleware or proxies.

For most use cases, API key authentication via the `Authorization` header is sufficient.

## Error Responses

### Missing API Key

If a mutating endpoint is called without an API key:

**`401 Unauthorized`**

```json
{
  "error": "unauthorized",
  "message": "Missing or invalid API key"
}
```

### Invalid API Key

If the provided API key does not match any entity:

**`401 Unauthorized`**

```json
{
  "error": "unauthorized",
  "message": "Missing or invalid API key"
}
```

### Insufficient Permissions

If the authenticated entity does not have permission for the requested action (e.g., trying to update a promise they are not party to):

**`403 Forbidden`**

```json
{
  "error": "forbidden",
  "message": "You do not have permission to perform this action"
}
```

## Security Best Practices

1. **Store keys securely.** Use environment variables or a secrets manager. Never hardcode API keys in source code.
2. **Rotate keys if compromised.** If you suspect a key has been leaked, contact the Soz Ledger team to issue a replacement.
3. **Use HTTPS only.** All API requests must be made over HTTPS. HTTP requests will be rejected.
4. **Limit key access.** In multi-agent deployments, give each agent its own entity and key rather than sharing a single key across agents.
5. **Monitor usage.** Watch for unexpected spikes in API usage that could indicate a compromised key.
