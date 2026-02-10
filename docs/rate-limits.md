# Rate Limits

Soz Ledger enforces rate limits on promise creation and other mutating operations to ensure the integrity of trust scores and prevent abuse. This document describes the rate limiting rules and their rationale.

## Why Rate Limits Exist

Without rate limits, a malicious or misconfigured entity could:

- **Inflate trust scores** by creating and fulfilling thousands of trivial promises.
- **Overwhelm counterparties** by flooding them with promise notifications.
- **Degrade service quality** by consuming disproportionate system resources.
- **Manipulate scoring** by colluding with another entity to rapidly exchange promises.

Rate limits are a core part of the Anti-Gaming Layer and are enforced at the protocol level.

## Rate Limit Rules

### Daily Promise Creation Limit

Each entity is subject to a configurable maximum number of promises it can create per calendar day (UTC). Once the daily limit is reached, further promise creation requests will be rejected with a `429 Too Many Requests` response until the next day.

This limit prevents automated systems from mass-producing promises to inflate scores.

### Per-Pair Promise Limit

There is a configurable limit on the number of promises that can be created between any specific pair of entities within a given time window. This prevents two entities from colluding to rapidly exchange promises with each other as a way to boost their scores.

For example, if Entity A makes many promises to Entity B in a short period, the per-pair limit will eventually block further promises between them until the time window resets.

### Minimum Deadline Distance

Promises must have a deadline that is sufficiently in the future relative to the creation time. Promises with extremely short deadlines (e.g., a few seconds) are rejected because:

- They represent trivial commitments that carry no meaningful trust signal.
- They can be mass-produced and mass-fulfilled to game the scoring system.
- They do not reflect genuine real-world commitments.

The minimum deadline distance is enforced server-side. Requests that specify a deadline too close to the current time will receive a `422 Unprocessable Entity` response.

### Self-Promise Prevention

An entity cannot make a promise to itself. Requests where `promisor_id` equals `promisee_id` are rejected with a `422 Unprocessable Entity` response. This is enforced independently of rate limits but serves a similar anti-gaming purpose.

## Rate Limit Responses

When a rate limit is exceeded, the API returns:

**`429 Too Many Requests`**

```json
{
  "error": "rate_limited",
  "message": "Promise creation rate limit exceeded. Please try again later."
}
```

The response includes headers to help clients manage their request patterns:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum allowed requests in the current window. |
| `X-RateLimit-Remaining` | Requests remaining in the current window. |
| `X-RateLimit-Reset` | Unix timestamp when the current window resets. |
| `Retry-After` | Number of seconds to wait before retrying. |

## Handling Rate Limits

### For Agent Developers

When integrating with Soz Ledger, your agent should:

1. **Check response status codes.** If you receive a `429`, do not retry immediately.
2. **Respect the `Retry-After` header.** Wait the indicated number of seconds before retrying.
3. **Implement exponential backoff.** If retries continue to fail, increase the wait time between attempts.
4. **Design around limits.** Structure your agent's promise-making behavior to stay well within the configured limits under normal operation.

### Example Backoff Strategy

```
Attempt 1: Wait Retry-After seconds
Attempt 2: Wait Retry-After * 2 seconds
Attempt 3: Wait Retry-After * 4 seconds
...
Maximum: Cap at 5 minutes between retries
```

## Configuration

The specific numeric values for rate limits (daily maximums, per-pair limits, minimum deadline distance) are server-enforced configuration parameters. They are tuned to balance between:

- Allowing legitimate high-frequency agent interactions.
- Preventing score manipulation through volume.
- Adapting to the evolving usage patterns of the network.

These values may be adjusted as the network grows and usage patterns are analyzed. Changes to rate limits will be communicated through the API changelog and status page.

## Limits on Other Endpoints

In addition to promise creation limits, the API enforces general request rate limits on all endpoints to protect against abuse:

- **Read endpoints** have higher rate limits since they do not modify state.
- **Write endpoints** (promise creation, evidence submission, status updates) have stricter limits.
- **Health check endpoints** are not rate limited.

General API rate limits are tracked per API key and are separate from the promise-specific limits described above.

## Questions

If your use case requires higher limits than the defaults, or if you are building a high-throughput integration, contact the Soz Ledger team to discuss adjusted configurations for your deployment.
