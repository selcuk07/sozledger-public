# Soz Ledger

**AI Agent Trust Protocol** -- Track, verify, and score agent promises.

Soz Ledger is an open protocol for building trust between AI agents, humans, and organizations. Agents make promises, provide evidence, and earn trust scores based on their track record.

## How It Works

1. **Entities** register (agents, humans, or orgs)
2. **Promises** are created between entities with deadlines and categories
3. **Evidence** is submitted to prove promise fulfillment
4. **Trust Scores** are calculated based on promise history

## Quick Start

### Python SDK

```bash
pip install soz-ledger
```

```python
from soz_ledger import SozLedgerClient

client = SozLedgerClient(api_key="your_api_key")

# Register an agent
agent = client.entities.create(
    name="DataFetchBot",
    type="agent",
    metadata={"platform": "langchain", "version": "1.0"}
)

# Create a promise
promise = client.promises.create(
    promisor_id=agent.id,
    promisee_id="user_abc",
    description="Fetch and deliver report within 30 seconds",
    deadline="2026-02-10T15:00:00Z",
    category="delivery"
)

# Submit evidence and fulfill
client.evidence.submit(
    promise_id=promise.id,
    type="api_callback",
    submitted_by=agent.id,
    payload={"status": 200, "delivered_at": "2026-02-10T14:59:45Z"}
)
client.promises.fulfill(promise.id)

# Check trust score
score = client.scores.get(agent.id)
print(f"Trust Score: {score.overall_score}")  # 0.85
print(f"Level: {score.level}")                # "Highly Trusted"
```

## Documentation

- [Whitepaper](docs/whitepaper.md) -- Concept, architecture, use cases
- [Protocol Spec](docs/protocol-spec.md) -- Data model and state machine
- [API Reference](docs/api-reference.md) -- Endpoint documentation
- [Authentication](docs/authentication.md) -- Auth flow
- [Trust Levels](docs/trust-levels.md) -- Score levels and meanings
- [Webhooks](docs/webhooks.md) -- Event type catalog
- [Rate Limits](docs/rate-limits.md) -- Usage rules

## Protocol

The protocol is defined via an [OpenAPI 3.1 spec](protocol/openapi.yaml) and [JSON Schemas](protocol/schemas/).

## SDKs

| Language | Status | Path |
|----------|--------|------|
| Python | Stable | [sdk/python](sdk/python/) |
| JavaScript/TypeScript | Stub | [sdk/javascript](sdk/javascript/) |

## Examples

- [Python Quickstart](examples/python/quickstart.py)
- [Agent Integration](examples/python/agent_integration.py)
- [Webhook Receiver](examples/python/webhook_receiver.py)
- [JavaScript Quickstart](examples/javascript/quickstart.js)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT -- see [LICENSE](LICENSE).
