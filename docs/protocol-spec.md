# Protocol Specification

This document defines the data models, state machines, and rules that constitute the Soz Ledger AI Agent Trust Protocol.

## Data Models

### Entity

An Entity represents any participant in the trust network.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique identifier for the entity. Assigned by the system on creation. |
| `name` | string | Display name of the entity. Must be between 1 and 200 characters. |
| `entity_type` | enum | The type of entity. One of: `agent`, `human`, `org`. |
| `metadata` | object | Optional key-value metadata associated with the entity (e.g., platform, version, description). |
| `created_at` | datetime (ISO 8601) | Timestamp of entity creation. |
| `updated_at` | datetime (ISO 8601) | Timestamp of last update. |

#### Entity Types

- **`agent`** -- An autonomous AI agent that acts on behalf of a user or organization.
- **`human`** -- A human participant interacting directly with the trust network.
- **`org`** -- An organization that may operate multiple agents or human participants.

---

### Promise

A Promise represents a commitment from one entity (the promisor) to another entity (the promisee).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique identifier for the promise. Assigned by the system on creation. |
| `promisor_id` | string (UUID) | The entity making the promise. |
| `promisee_id` | string (UUID) | The entity to whom the promise is made. |
| `description` | string | Human-readable description of the promise. Must be between 1 and 1000 characters. |
| `category` | enum | The category of the promise. See Promise Categories below. |
| `status` | enum | Current status in the promise lifecycle. See Promise Lifecycle below. |
| `deadline` | datetime (ISO 8601) | The deadline by which the promise must be fulfilled. Must be in the future and sufficiently far from creation time (see rate limits). |
| `fulfilled_at` | datetime (ISO 8601) | Timestamp when the promise was fulfilled. Null if not yet fulfilled. |
| `broken_at` | datetime (ISO 8601) | Timestamp when the promise was marked as broken. Null if not broken. |
| `created_at` | datetime (ISO 8601) | Timestamp of promise creation. |
| `updated_at` | datetime (ISO 8601) | Timestamp of last update. |

#### Promise Categories

| Category | Description |
|----------|-------------|
| `delivery` | A promise to deliver a specific artifact, result, or output by the deadline. |
| `payment` | A promise to complete a payment or financial transfer by the deadline. |
| `response` | A promise to respond to a request or inquiry by the deadline. |
| `uptime` | A promise to maintain availability or uptime through the deadline. |
| `custom` | A promise that does not fit the predefined categories. Must include a clear description. |

#### Validation Rules

- The `promisor_id` and `promisee_id` must refer to existing entities.
- The `promisor_id` and `promisee_id` must not be the same (self-promises are not allowed).
- The `deadline` must be in the future, with a minimum distance from the creation time enforced by the server to prevent trivial promises.
- Promise creation is subject to rate limits (see [Rate Limits](rate-limits.md)).

---

### Evidence

Evidence is an artifact or reference attached to a promise to support verification of its outcome.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique identifier for the evidence. Assigned by the system on creation. |
| `promise_id` | string (UUID) | The promise this evidence is associated with. |
| `submitted_by` | string (UUID) | The entity that submitted this evidence. |
| `evidence_type` | enum | The type of evidence. See Evidence Types below. |
| `content` | string | The evidence content. Interpretation depends on `evidence_type`. |
| `metadata` | object | Optional additional metadata about the evidence. |
| `created_at` | datetime (ISO 8601) | Timestamp of evidence submission. |

#### Evidence Types

| Type | Description | Content Format |
|------|-------------|----------------|
| `api_callback` | The outcome was reported via an automated API callback. | Callback URL or response payload reference. |
| `webhook` | The outcome was reported via a webhook event. | Webhook event identifier or payload reference. |
| `manual` | The outcome was reported manually by a participant. | Free-text description of the evidence. |
| `file` | A file artifact serves as evidence. | File URL or file reference identifier. |
| `link` | An external link serves as evidence. | URL pointing to the external evidence. |

---

### TrustScore

A TrustScore represents the computed trust rating for an entity at a point in time.

| Field | Type | Description |
|-------|------|-------------|
| `entity_id` | string (UUID) | The entity this score belongs to. |
| `score` | float | The computed trust score, ranging from 0.00 to 1.00. |
| `level` | string | The human-readable trust level (see [Trust Levels](trust-levels.md)). |
| `total_promises` | integer | Total number of promises made by this entity. |
| `fulfilled_count` | integer | Number of promises fulfilled. |
| `broken_count` | integer | Number of promises broken. |
| `active_count` | integer | Number of currently active promises. |
| `expired_count` | integer | Number of promises that expired without resolution. |
| `disputed_count` | integer | Number of promises currently in dispute. |
| `is_rated` | boolean | Whether the entity has met the minimum promise threshold to receive a public rating. |
| `computed_at` | datetime (ISO 8601) | Timestamp when this score was computed. |

#### Scoring Notes

- The scoring algorithm considers promise outcomes, recency, category, and counterparty diversity.
- Entities that have not met the minimum activity threshold are marked as `is_rated: false` and display a trust level of "Unrated".
- The internal scoring formula and its parameters are not part of the public protocol specification.
- Score history is retained, allowing participants to observe trust trends over time.

---

## Promise Lifecycle

A promise follows a strict state machine. The following diagram describes valid state transitions:

```
                  +-----------+
                  |           |
     +----------->  active    +----------+----------+
     |            |           |          |          |
  (created)       +-----+-----+          |          |
                        |                |          |
                        |                |          |
                  +-----v-----+   +------v----+    |
                  |           |   |           |    |
                  | fulfilled |   |  broken   |    |
                  |           |   |           |    |
                  +-----------+   +-----------+    |
                                                   |
                  +-----------+   +-----------+    |
                  |           |   |           |    |
                  |  expired  |   | disputed  +<---+
                  |           |   |           |
                  +-----^-----+   +-----+-----+
                        |               |
                        |               |
                  (deadline passes,     +----> resolved as
                   no action taken)            fulfilled or broken
```

### States

| State | Description |
|-------|-------------|
| `active` | The promise has been created and the deadline has not yet passed. This is the initial state. |
| `fulfilled` | The promisor has fulfilled the promise before the deadline. Terminal state. |
| `broken` | The promise has been marked as broken (either explicitly or by the system). Terminal state. |
| `expired` | The deadline passed without the promise being fulfilled or explicitly broken. The system automatically transitions active promises to expired when their deadline passes. Terminal state. |
| `disputed` | One of the parties has disputed the promise outcome. Requires resolution. |

### Valid Transitions

| From | To | Trigger |
|------|----|---------|
| `active` | `fulfilled` | The promisor or an authorized party marks the promise as fulfilled before the deadline. |
| `active` | `broken` | The promisor or an authorized party marks the promise as broken. |
| `active` | `expired` | The system automatically expires the promise when the deadline passes without action. |
| `active` | `disputed` | Either the promisor or promisee raises a dispute on the promise. |
| `disputed` | `fulfilled` | The dispute is resolved in favor of fulfillment. |
| `disputed` | `broken` | The dispute is resolved as broken. |

### Invalid Transitions

- A `fulfilled` promise cannot change to any other state.
- A `broken` promise cannot change to any other state.
- An `expired` promise cannot change to any other state.
- A promise cannot transition directly from `fulfilled` to `broken` or vice versa.
- A promise cannot return to `active` from any terminal state.

---

## Protocol Constraints

### Identity

- Each entity has a globally unique UUID.
- Entity names are not required to be unique (multiple entities can share a name).
- API keys are bound to entities and must be kept secret.

### Immutability

- Once a promise is created, its `promisor_id`, `promisee_id`, `description`, `category`, and `deadline` are immutable.
- Evidence, once submitted, cannot be modified or deleted.
- Score history entries are append-only.

### Time

- All timestamps are in UTC and formatted as ISO 8601.
- The server's clock is authoritative for deadline enforcement and expiration.
- Promise deadlines are evaluated at the second granularity.

### Rate Limiting

- Promise creation is subject to configurable rate limits to prevent abuse and score inflation.
- Specific limits are documented in [Rate Limits](rate-limits.md).

---

## Versioning

This specification describes **version 1** of the Soz Ledger protocol. The API uses a `/v1/` prefix for all endpoints. Future versions will be introduced under new prefixes (e.g., `/v2/`) with a documented migration path.
