# Soz Ledger

**AI Agent Trust Protocol** -- Track, verify, and score agent promises.

[View Landing Page](site/index.html) | [Open Dashboard](dashboard/index.html)

Soz Ledger is an open protocol for building trust between AI agents, humans, and organizations. Agents make promises, provide evidence, and earn verifiable trust levels based on their track record.

The **protocol and data model are open**. The scoring engine is intentionally abstracted -- implementations may use different scoring strategies while sharing the same promise graph and evidence layer.

## Why Use Soz Ledger?

- **Portable trust across platforms.** An agent's trust level follows it everywhere. No more starting from zero on every new platform.
- **Verifiable promise history.** Every claim is backed by evidence and counterparty confirmation -- not self-reported ratings.
- **Better agent selection and pricing.** Platforms, workflows, and marketplaces can use trust levels to gate access, route tasks, and justify premium pricing for reliable agents.

## Built For

- **Agent builders** -- give your agents a portable reputation that works across platforms
- **Workflow orchestrators** -- gate task routing on trust levels instead of static allow-lists
- **AI marketplaces** -- display verified trust badges alongside agent listings

## How It Works

1. **Entities** register (agents, humans, or orgs)
2. **Promises** are created between entities with deadlines and categories
3. **Evidence** is submitted to prove promise fulfillment
4. **Trust Levels** are calculated based on promise history, counterparty diversity, and category performance

Not all promises are weighted equally. The scoring system accounts for counterparty diversity, promise category, recency, and fulfillment timing. Self-dealing patterns, velocity anomalies, and low-quality counterparties are detected and down-weighted. See [Anti-Gaming](docs/whitepaper.md) in the whitepaper for details.

Trust is not a single number -- it is a multi-dimensional profile. Each entity has an overall level plus per-category breakdowns (delivery, payment, response, uptime). See [Trust Levels](docs/trust-levels.md) for the full model.

## Production API

The Soz Ledger engine is live:

| Resource | URL |
|----------|-----|
| API Base | https://api-production-c4c8.up.railway.app |
| Swagger UI | https://api-production-c4c8.up.railway.app/docs |
| Health Check | https://api-production-c4c8.up.railway.app/health |

## Quick Start

### Python SDK

```bash
pip install soz-ledger
```

```python
from soz_ledger import SozLedgerClient

client = SozLedgerClient(
    api_key="your_api_key",
    base_url="https://api-production-c4c8.up.railway.app",
)

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

# Check trust level
score = client.scores.get(agent.id)
print(f"Level: {score.level}")  # "Highly Trusted"
```

### Webhook Setup

```python
# Register a webhook to receive real-time events
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/soz",
    event_types=["promise.created", "promise.fulfilled", "promise.broken"],
)
print(f"Webhook secret: {webhook.secret}")  # Save this for signature verification

# List your webhooks
webhooks = client.webhooks.list()

# Check delivery logs
logs = client.webhooks.logs(webhook.id)
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

The protocol is defined via an [OpenAPI 3.1 spec](protocol/openapi.yaml) and [JSON Schemas](protocol/schemas/). The protocol follows semantic versioning; backward compatibility is preserved within major versions.

## SDKs

| Language | Status | Path |
|----------|--------|------|
| Python | Stable | [sdk/python](sdk/python/) |
| JavaScript/TypeScript | Stable | [sdk/javascript](sdk/javascript/) |

## Integrations

| Framework | Package | Install |
|-----------|---------|---------|
| LangChain | [soz-ledger-langchain](integrations/langchain/) | `pip install soz-ledger-langchain` |
| CrewAI | [soz-ledger-crewai](integrations/crewai/) | `pip install soz-ledger-crewai` |

**LangChain** -- every tool call becomes a promise:

```python
from soz_ledger_langchain import SozLedgerCallbackHandler

handler = SozLedgerCallbackHandler(client, agent_entity_id="ent_abc")
agent.invoke({"input": "..."}, config={"callbacks": [handler]})
```

**CrewAI** -- every completed task becomes a promise:

```python
from soz_ledger_crewai import soz_task_callback

callback = soz_task_callback(client, agent_entity_id="ent_abc")
task = Task(description="...", callback=callback)
```

## Examples

- [Python Quickstart](examples/python/quickstart.py)
- [Agent Integration](examples/python/agent_integration.py)
- [LangChain Integration](examples/python/langchain_integration.py)
- [CrewAI Integration](examples/python/crewai_integration.py)
- [Webhook Receiver](examples/python/webhook_receiver.py)
- [JavaScript Quickstart](examples/javascript/quickstart.js)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT -- see [LICENSE](LICENSE).

This repository is the reference implementation. The official trust graph and scoring services are operated by Soz Ledger.
