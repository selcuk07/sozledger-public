# Soz Ledger: An AI Agent Trust Protocol

## Abstract

Soz Ledger is a trust protocol designed for autonomous AI agents, humans, and organizations to establish, measure, and verify trust through a system of accountable promises. In a world where AI agents increasingly interact with each other and with humans on behalf of their operators, there is no standardized way to determine whether an agent is trustworthy. Soz Ledger solves this by creating an immutable, verifiable ledger of promises made and kept -- producing a reputation score that any participant can query before engaging in a transaction.

## The Problem

As AI agents become more autonomous -- negotiating deals, executing tasks, managing workflows -- a fundamental question arises: **How do you trust an agent you have never interacted with before?**

Today, trust between agents is either assumed (dangerous), delegated to centralized gatekeepers (fragile), or simply absent (limiting). There is no open, decentralized mechanism for agents to build reputation based on actual behavior.

This creates several concrete problems:

- **No accountability for agent behavior.** An agent can promise to deliver a result, fail, and face no lasting consequence.
- **No portable reputation.** An agent that performs reliably on one platform has no way to carry that reputation to another.
- **No basis for automated trust decisions.** Agents cannot programmatically evaluate whether to engage with an unfamiliar counterpart.
- **No fraud deterrence.** Without a record of past behavior, bad actors can repeatedly exploit the system with new identities.

## The Solution

Soz Ledger introduces a **promise-based trust protocol** in which any entity (AI agent, human, or organization) can:

1. **Register** as a participant in the trust network.
2. **Make promises** to other participants, with defined deadlines and categories.
3. **Fulfill or break** those promises, with the outcome recorded permanently.
4. **Submit evidence** to verify promise outcomes.
5. **Earn a trust score** that reflects their track record of keeping promises.

The trust score is a single, queryable number between 0.00 and 1.00 that any other participant can check before deciding to engage. Scores are computed by the protocol's Trust Engine based on the full history of an entity's promises.

## Core Principles

### Promise-Centric Trust

Trust is not declared -- it is earned. Every interaction that matters is modeled as a promise: a commitment from one entity to another, with a clear deadline and a verifiable outcome. This makes trust concrete and measurable.

### Transparency Without Exposure

Trust scores and promise histories are queryable by any participant, enabling informed decisions. However, the internal scoring algorithms and anti-gaming thresholds remain protected to prevent manipulation.

### Category-Aware Scoring

Not all promises are equal. A promise to deliver a software artifact carries different weight than a promise to respond within five minutes. Soz Ledger categorizes promises (delivery, payment, response, uptime, and custom) and accounts for these differences in its scoring model.

### Anti-Gaming by Design

The protocol includes multiple layers of protection against score manipulation, including rate limits, trivial promise detection, relationship-pair tracking, and time-decay mechanisms. These are enforced at the protocol level, not as optional add-ons.

## Architecture Overview

Soz Ledger is composed of four primary layers:

### Protocol Layer

The Protocol Layer defines the data models and state machines that govern how entities, promises, and evidence interact. It specifies:

- How entities are registered and identified.
- The lifecycle of a promise (creation, fulfillment, breaking, expiration, dispute).
- How evidence is attached to promises.
- The rules for valid state transitions.

This layer is the public contract of the system. Any conforming implementation must respect these rules.

### Trust Engine

The Trust Engine is responsible for computing trust scores from raw promise data. It considers:

- The ratio of fulfilled to broken promises.
- The recency of promise outcomes (recent behavior is weighted more heavily).
- The category of each promise.
- The diversity of counterparties (promises kept across many relationships are more meaningful than promises kept with a single partner).

The Trust Engine's internal algorithm is intentionally opaque to prevent gaming. Only the inputs (promise outcomes) and outputs (trust scores) are part of the public protocol.

### Anti-Gaming Layer

The Anti-Gaming Layer enforces rules that prevent entities from artificially inflating their trust scores. These rules include:

- **Rate limiting** on promise creation (daily limits and per-relationship limits).
- **Trivial promise rejection** (promises with extremely short deadlines are blocked).
- **Self-promise prevention** (an entity cannot make promises to itself).
- **Minimum activity thresholds** (entities must have enough promise history before receiving a public score).
- **Probation periods** for new entities.

The specific thresholds and limits are server-enforced and not publicly disclosed.

### Data Layer

The Data Layer handles persistent storage of all protocol data: entities, promises, evidence, and computed scores. It provides:

- Durable storage with full audit history.
- Efficient querying for score computation and API responses.
- Score history tracking over time.

## Use Cases

### Agent-to-Agent Trust

Two AI agents that have never interacted can query each other's Soz Ledger trust scores before entering into a transaction. For example:

- **Agent A** needs to hire **Agent B** to perform a data processing task. Before committing, Agent A queries Agent B's trust score and sees a score of 0.87 (Highly Trusted) based on 200+ fulfilled promises. Agent A proceeds with confidence.
- **Agent C** encounters **Agent D** with a score of 0.22 (Low Trust) and decides to require escrow or additional verification before proceeding.

### Marketplace Reputation

Platforms that host AI agent services can integrate Soz Ledger as their reputation layer. Instead of building proprietary review systems, they can:

- Display Soz Ledger trust scores on agent profiles.
- Set minimum trust thresholds for premium listings.
- Allow buyers to filter agents by trust level.
- Provide portable reputation that follows agents across platforms.

### Automated Workflow Orchestration

In multi-agent workflows where agents are chained together (Agent A calls Agent B, which calls Agent C), Soz Ledger enables automated trust gates:

- A workflow engine can check each agent's trust score before routing a task.
- If an agent's score drops below a threshold, the workflow can automatically reroute to a backup agent.
- Promise creation and fulfillment can be integrated directly into the workflow, so trust scores update in real time.

### SLA Monitoring and Enforcement

Organizations can use Soz Ledger to track service-level agreements:

- Each SLA commitment is modeled as a promise with a deadline.
- Uptime promises, response-time promises, and delivery promises are tracked automatically.
- Trust scores provide a rolling summary of SLA compliance.

### Cross-Organization Trust

When organizations need to evaluate each other's AI agents for partnership or integration:

- Organization trust scores aggregate the behavior of all agents operating under that organization.
- A single query reveals whether an organization's agents collectively keep their commitments.

## Design Decisions

### Why Promises, Not Reviews?

Review-based systems are subjective, easily gamed, and require human input. Promise-based trust is objective: either the promise was fulfilled by the deadline, or it was not. This makes the system suitable for fully autonomous agents that operate without human oversight.

### Why a Single Score?

A single 0.00-1.00 score is easy to query, easy to compare, and easy to threshold against. Detailed breakdowns (by category, by time period, by counterparty) are available through the API for entities that need more nuance, but the headline score is deliberately simple.

### Why Opaque Scoring?

Publishing the exact scoring algorithm would allow bad actors to game the system optimally. By keeping the algorithm private while publishing the rules (what counts as a promise, what state transitions are valid, what anti-gaming protections exist), we maintain both transparency and security.

## Conclusion

Soz Ledger provides the missing trust layer for the emerging ecosystem of autonomous AI agents. By reducing trust to a simple, verifiable, promise-based protocol, it enables agents, humans, and organizations to interact with confidence -- even when they have no prior relationship. The protocol is open for integration, the API is straightforward, and the trust model is designed to be robust against manipulation from day one.
