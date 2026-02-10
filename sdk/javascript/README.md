# Soz Ledger -- JavaScript / TypeScript SDK

Zero-dependency TypeScript client for the Soz Ledger AI Agent Trust Protocol.
Requires Node 18+ or any runtime with a global `fetch` implementation.

## Installation

```bash
npm install soz-ledger
```

Or, if you are working from source:

```bash
cd sdk/javascript
npm install
npm run build
```

## Quick start

```ts
import { SozLedgerClient } from "soz-ledger";

const client = new SozLedgerClient("your_api_key", "http://localhost:8000");

// Register an agent entity
const agent = await client.entities.create({
  name: "my-agent",
  type: "agent",
});

// Create a promise
const promise = await client.promises.create({
  promisor_id: agent.id,
  promisee_id: "some-other-entity-id",
  description: "Deliver the weekly report",
  category: "delivery",
});

// Submit evidence
await client.evidence.submit(promise.id, {
  type: "webhook",
  submitted_by: agent.id,
  payload: { report: "..." },
});

// Fulfill the promise
await client.promises.fulfill(promise.id);

// Check the trust score
const score = await client.scores.get(agent.id);
console.log(score.level, score.overall_score);
```

## Error handling

```ts
import { SozLedgerClient, SozLedgerError } from "soz-ledger";

const client = new SozLedgerClient("your_api_key");

try {
  await client.entities.get("non-existent-id");
} catch (err) {
  if (err instanceof SozLedgerError) {
    console.error(err.status); // e.g. 404
    console.error(err.code);   // e.g. "not_found"
    console.error(err.body);   // full API error response
  }
}
```

## Available sub-APIs

| Sub-API              | Methods                                         |
| -------------------- | ------------------------------------------------ |
| `client.entities`    | `create`, `get`                                  |
| `client.promises`    | `create`, `get`, `fulfill`, `breakPromise`, `dispute` |
| `client.evidence`    | `submit`, `list`                                 |
| `client.scores`      | `get`, `history`                                 |

## TypeScript types

All request/response interfaces are exported from the package root:

```ts
import type { Entity, Promise, Evidence, TrustScore } from "soz-ledger";
```

## Contributing

This SDK is part of the [Soz Ledger](https://github.com/anthropics/sozledger-public) project. Contributions welcome -- see the main repo for guidelines.

## License

MIT
