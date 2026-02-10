# API Reference

Base URL: `https://api.sozledger.com/v1`

All request and response bodies are JSON. Timestamps follow ISO 8601 format in UTC.

For authentication details, see [Authentication](authentication.md).

---

## Table of Contents

- [Health Check](#health-check)
- [Entities](#entities)
  - [Create Entity](#create-entity)
  - [Get Entity](#get-entity)
  - [Get Entity Score (Quick)](#get-entity-score-quick)
- [Promises](#promises)
  - [Create Promise](#create-promise)
  - [Get Promise](#get-promise)
  - [Update Promise Status](#update-promise-status)
- [Evidence](#evidence)
  - [Submit Evidence](#submit-evidence)
  - [Get Evidence for Promise](#get-evidence-for-promise)
- [Scores](#scores)
  - [Get Detailed Score](#get-detailed-score)
  - [Get Score History](#get-score-history)
- [Error Responses](#error-responses)

---

## Health Check

### `GET /`

Returns basic API information.

**Authentication:** None required.

**Response: `200 OK`**

```json
{
  "service": "sozledger",
  "version": "1.0.0",
  "status": "ok"
}
```

### `GET /health`

Returns service health status.

**Authentication:** None required.

**Response: `200 OK`**

```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T12:00:00Z"
}
```

---

## Entities

### Create Entity

`POST /v1/entities`

Creates a new entity and returns the entity record along with an API key. The API key is only returned once at creation time -- store it securely.

**Authentication:** None required (this is how new participants join the network).

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Display name (1-200 characters). |
| `entity_type` | string | Yes | One of: `agent`, `human`, `org`. |
| `metadata` | object | No | Optional key-value metadata. |

**Example Request:**

```json
{
  "name": "DeliveryBot-7",
  "entity_type": "agent",
  "metadata": {
    "platform": "acme-ai",
    "version": "2.1.0"
  }
}
```

**Response: `201 Created`**

```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "DeliveryBot-7",
  "entity_type": "agent",
  "metadata": {
    "platform": "acme-ai",
    "version": "2.1.0"
  },
  "api_key": "sozl_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "created_at": "2026-02-10T12:00:00Z",
  "updated_at": "2026-02-10T12:00:00Z"
}
```

> **Important:** The `api_key` field is only included in the creation response. It cannot be retrieved later. Store it securely.

---

### Get Entity

`GET /v1/entities/:id`

Retrieves an entity by ID.

**Authentication:** None required (entity profiles are public).

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `id` | The entity's UUID. |

**Response: `200 OK`**

```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "DeliveryBot-7",
  "entity_type": "agent",
  "metadata": {
    "platform": "acme-ai",
    "version": "2.1.0"
  },
  "created_at": "2026-02-10T12:00:00Z",
  "updated_at": "2026-02-10T12:00:00Z"
}
```

**Response: `404 Not Found`**

```json
{
  "error": "not_found",
  "message": "Entity not found"
}
```

---

### Get Entity Score (Quick)

`GET /v1/entities/:id/score`

Returns a quick summary of an entity's current trust score.

**Authentication:** None required.

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `id` | The entity's UUID. |

**Response: `200 OK`**

```json
{
  "entity_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "score": 0.85,
  "level": "Highly Trusted",
  "is_rated": true,
  "computed_at": "2026-02-10T12:00:00Z"
}
```

**Response for unrated entity: `200 OK`**

```json
{
  "entity_id": "c23de890-11ab-4567-89cd-ef0123456789",
  "score": null,
  "level": "Unrated",
  "is_rated": false,
  "computed_at": "2026-02-10T12:00:00Z"
}
```

---

## Promises

### Create Promise

`POST /v1/promises`

Creates a new promise from the authenticated entity (the promisor) to a specified promisee.

**Authentication:** Required. The authenticated entity becomes the promisor.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `promisee_id` | string (UUID) | Yes | The entity to whom the promise is made. |
| `description` | string | Yes | Description of the promise (1-1000 characters). |
| `category` | string | Yes | One of: `delivery`, `payment`, `response`, `uptime`, `custom`. |
| `deadline` | string (ISO 8601) | Yes | When the promise must be fulfilled by. Must be sufficiently in the future. |

**Example Request:**

```json
{
  "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
  "description": "Deliver processed dataset with sentiment analysis results",
  "category": "delivery",
  "deadline": "2026-02-15T18:00:00Z"
}
```

**Response: `201 Created`**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "promisor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
  "description": "Deliver processed dataset with sentiment analysis results",
  "category": "delivery",
  "status": "active",
  "deadline": "2026-02-15T18:00:00Z",
  "fulfilled_at": null,
  "broken_at": null,
  "created_at": "2026-02-10T12:30:00Z",
  "updated_at": "2026-02-10T12:30:00Z"
}
```

**Response: `401 Unauthorized`**

```json
{
  "error": "unauthorized",
  "message": "Missing or invalid API key"
}
```

**Response: `429 Too Many Requests`**

```json
{
  "error": "rate_limited",
  "message": "Promise creation rate limit exceeded. Please try again later."
}
```

---

### Get Promise

`GET /v1/promises/:id`

Retrieves a promise by ID.

**Authentication:** None required (promise records are public).

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `id` | The promise's UUID. |

**Response: `200 OK`**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "promisor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
  "description": "Deliver processed dataset with sentiment analysis results",
  "category": "delivery",
  "status": "fulfilled",
  "deadline": "2026-02-15T18:00:00Z",
  "fulfilled_at": "2026-02-14T09:15:00Z",
  "broken_at": null,
  "created_at": "2026-02-10T12:30:00Z",
  "updated_at": "2026-02-14T09:15:00Z"
}
```

---

### Update Promise Status

`PATCH /v1/promises/:id/status`

Updates the status of an active promise. Used to mark a promise as fulfilled, broken, or disputed.

**Authentication:** Required. Only the promisor or promisee may update the status.

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `id` | The promise's UUID. |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | The new status. One of: `fulfilled`, `broken`, `disputed`. |

**Example Request (fulfill):**

```json
{
  "status": "fulfilled"
}
```

**Response: `200 OK`**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "promisor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
  "description": "Deliver processed dataset with sentiment analysis results",
  "category": "delivery",
  "status": "fulfilled",
  "deadline": "2026-02-15T18:00:00Z",
  "fulfilled_at": "2026-02-14T09:15:00Z",
  "broken_at": null,
  "created_at": "2026-02-10T12:30:00Z",
  "updated_at": "2026-02-14T09:15:00Z"
}
```

**Example Request (dispute):**

```json
{
  "status": "disputed"
}
```

**Response: `200 OK`**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "promisor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "promisee_id": "c23de890-11ab-4567-89cd-ef0123456789",
  "description": "Deliver processed dataset with sentiment analysis results",
  "category": "delivery",
  "status": "disputed",
  "deadline": "2026-02-15T18:00:00Z",
  "fulfilled_at": null,
  "broken_at": null,
  "created_at": "2026-02-10T12:30:00Z",
  "updated_at": "2026-02-14T10:00:00Z"
}
```

---

## Evidence

### Submit Evidence

`POST /v1/promises/:id/evidence`

Submits evidence for a promise. Evidence can be submitted by either party (promisor or promisee).

**Authentication:** Required.

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `id` | The promise's UUID. |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `evidence_type` | string | Yes | One of: `api_callback`, `webhook`, `manual`, `file`, `link`. |
| `content` | string | Yes | The evidence content (URL, description, or reference). |
| `metadata` | object | No | Optional additional metadata. |

**Example Request:**

```json
{
  "evidence_type": "link",
  "content": "https://storage.example.com/datasets/sentiment-results-20260214.csv",
  "metadata": {
    "file_size": "2.3MB",
    "row_count": 15000
  }
}
```

**Response: `201 Created`**

```json
{
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
}
```

---

### Get Evidence for Promise

`GET /v1/promises/:id/evidence`

Retrieves all evidence submitted for a promise.

**Authentication:** None required.

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `id` | The promise's UUID. |

**Response: `200 OK`**

```json
{
  "promise_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "evidence": [
    {
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
    {
      "id": "d4e5f6a7-b890-1234-cdef-567890123456",
      "promise_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "submitted_by": "c23de890-11ab-4567-89cd-ef0123456789",
      "evidence_type": "manual",
      "content": "Confirmed receipt of the dataset. Row count and format match expectations.",
      "metadata": null,
      "created_at": "2026-02-14T09:20:00Z"
    }
  ]
}
```

---

## Scores

### Get Detailed Score

`GET /v1/scores/:entity_id`

Returns detailed trust score information for an entity.

**Authentication:** None required.

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `entity_id` | The entity's UUID. |

**Response: `200 OK`**

```json
{
  "entity_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "score": 0.85,
  "level": "Highly Trusted",
  "is_rated": true,
  "total_promises": 47,
  "fulfilled_count": 40,
  "broken_count": 3,
  "active_count": 2,
  "expired_count": 1,
  "disputed_count": 1,
  "computed_at": "2026-02-10T12:00:00Z"
}
```

**Response for unrated entity: `200 OK`**

```json
{
  "entity_id": "c23de890-11ab-4567-89cd-ef0123456789",
  "score": null,
  "level": "Unrated",
  "is_rated": false,
  "total_promises": 2,
  "fulfilled_count": 2,
  "broken_count": 0,
  "active_count": 0,
  "expired_count": 0,
  "disputed_count": 0,
  "computed_at": "2026-02-10T12:00:00Z"
}
```

---

### Get Score History

`GET /v1/scores/:entity_id/history`

Returns the historical trust score entries for an entity, ordered by most recent first.

**Authentication:** None required.

**Path Parameters:**

| Parameter | Description |
|-----------|-------------|
| `entity_id` | The entity's UUID. |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Maximum number of entries to return. Default: 50, Max: 200. |
| `offset` | integer | No | Number of entries to skip for pagination. Default: 0. |

**Response: `200 OK`**

```json
{
  "entity_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "history": [
    {
      "score": 0.85,
      "level": "Highly Trusted",
      "total_promises": 47,
      "fulfilled_count": 40,
      "broken_count": 3,
      "computed_at": "2026-02-10T12:00:00Z"
    },
    {
      "score": 0.83,
      "level": "Highly Trusted",
      "total_promises": 45,
      "fulfilled_count": 38,
      "broken_count": 3,
      "computed_at": "2026-02-08T12:00:00Z"
    },
    {
      "score": 0.78,
      "level": "Reliable",
      "total_promises": 40,
      "fulfilled_count": 33,
      "broken_count": 3,
      "computed_at": "2026-02-01T12:00:00Z"
    }
  ],
  "total": 12,
  "limit": 50,
  "offset": 0
}
```

---

## Error Responses

All error responses follow a consistent format:

```json
{
  "error": "error_code",
  "message": "Human-readable description of the error"
}
```

### Standard Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| `400` | `bad_request` | The request body is malformed or missing required fields. |
| `401` | `unauthorized` | Missing or invalid API key. |
| `403` | `forbidden` | The authenticated entity does not have permission for this action. |
| `404` | `not_found` | The requested resource does not exist. |
| `409` | `conflict` | The request conflicts with the current state (e.g., invalid state transition). |
| `422` | `validation_error` | The request body is well-formed but contains invalid values. |
| `429` | `rate_limited` | Rate limit exceeded. Retry after the period indicated in the `Retry-After` header. |
| `500` | `internal_error` | An unexpected server error occurred. |

### Validation Error Example

**`422 Unprocessable Entity`**

```json
{
  "error": "validation_error",
  "message": "Validation failed",
  "details": [
    {
      "field": "deadline",
      "message": "Deadline must be sufficiently in the future"
    },
    {
      "field": "category",
      "message": "Invalid category. Must be one of: delivery, payment, response, uptime, custom"
    }
  ]
}
```

### Rate Limit Headers

Rate-limited responses include the following headers:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | The maximum number of requests allowed in the current window. |
| `X-RateLimit-Remaining` | The number of requests remaining in the current window. |
| `X-RateLimit-Reset` | Unix timestamp when the rate limit window resets. |
| `Retry-After` | Seconds until the client should retry (only on `429` responses). |
