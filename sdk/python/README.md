# Soz Ledger Python SDK

Official Python SDK for the Soz Ledger AI Agent Trust Protocol.

## Installation

```bash
pip install soz-ledger
```

## Quick Start

```python
from soz_ledger import SozLedgerClient

client = SozLedgerClient(api_key="your_api_key")

# Create an entity
agent = client.entities.create(
    name="MyAgent",
    type="agent",
    metadata={"platform": "langchain"}
)

# Create a promise
promise = client.promises.create(
    promisor_id=agent.id,
    promisee_id="other_entity_id",
    description="Deliver results within 1 hour",
    category="delivery"
)

# Fulfill the promise
client.promises.fulfill(promise.id)

# Check trust score
score = client.scores.get(agent.id)
print(f"{score.level}: {score.overall_score}")
```

## API Reference

### `SozLedgerClient(api_key, base_url="http://localhost:8000")`

Main client. Provides access to:

- `client.entities` -- Create and query entities
- `client.promises` -- Create, fulfill, break, or dispute promises
- `client.evidence` -- Submit and list evidence
- `client.scores` -- Query trust scores and history

### Entities

| Method | Description |
|--------|-------------|
| `entities.create(name, type, public_key=None, metadata=None)` | Register a new entity |
| `entities.get(entity_id)` | Get entity details |
| `entities.score(entity_id)` | Get entity trust score |

### Promises

| Method | Description |
|--------|-------------|
| `promises.create(promisor_id, promisee_id, description, deadline=None, category="custom")` | Create a promise |
| `promises.get(promise_id)` | Get promise details |
| `promises.fulfill(promise_id)` | Mark promise as fulfilled |
| `promises.break_promise(promise_id)` | Mark promise as broken |
| `promises.dispute(promise_id)` | Mark promise as disputed |

### Evidence

| Method | Description |
|--------|-------------|
| `evidence.submit(promise_id, type, submitted_by, payload=None)` | Submit evidence |
| `evidence.list(promise_id)` | List evidence for a promise |

### Scores

| Method | Description |
|--------|-------------|
| `scores.get(entity_id)` | Get detailed trust score |
| `scores.history(entity_id)` | Get score history |

## Requirements

- Python 3.11+
- httpx >= 0.25.0

## License

MIT
