# Soz Ledger -- JavaScript / TypeScript SDK

> **Status: stub / work-in-progress.**
> Method signatures are defined and types are complete, but the HTTP layer is
> not yet wired up. All methods currently throw a "Not implemented yet" error.

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
  type: "ai_agent",
});

// Create a promise
const promise = await client.promises.create({
  promisor_id: agent.id,
  promisee_id: "some-other-entity-id",
  description: "Deliver the weekly report",
  category: "task_completion",
});

// Submit evidence
await client.evidence.submit(promise.id, {
  type: "output",
  submitted_by: agent.id,
  payload: { report: "..." },
});

// Fulfill the promise
await client.promises.fulfill(promise.id);

// Check the trust score
const score = await client.scores.get(agent.id);
console.log(score.level, score.overall_score);
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
