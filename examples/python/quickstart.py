"""
Soz Ledger -- Quick Start Example
==================================
Demonstrates the basic trust lifecycle:
  register entity -> create promise -> submit evidence -> fulfill -> check score
"""

from soz_ledger import SozLedgerClient

# ── 1. Initialise the client ────────────────────────────────────────────────
#    Replace with your own API key and the URL of your Soz Ledger instance.
client = SozLedgerClient(
    api_key="your_api_key",
    base_url="http://localhost:8000",
)

# ── 2. Register two agent entities ──────────────────────────────────────────
#    Every participant in the trust graph is an "entity".
agent_a = client.entities.create(
    name="weather-agent",
    type="ai_agent",
)
print(f"Created agent entity: {agent_a.id}")

agent_b = client.entities.create(
    name="booking-agent",
    type="ai_agent",
)
print(f"Created agent entity: {agent_b.id}")

# ── 3. Create a promise from agent_a to agent_b ────────────────────────────
#    Promises are the core unit of accountability.  An agent declares
#    *what* it will do, *for whom*, and optionally *by when*.
promise = client.promises.create(
    promisor_id=agent_a.id,
    promisee_id=agent_b.id,
    description="Return a 5-day weather forecast in JSON format",
    category="data_delivery",
    deadline="2025-12-31T23:59:59Z",
)
print(f"Promise created: {promise.id}  status={promise.status}")

# ── 4. Submit evidence that work is being performed ─────────────────────────
#    Evidence is any verifiable artefact linked to a promise.
evidence = client.evidence.submit(
    promise_id=promise.id,
    type="output",
    submitted_by=agent_a.id,
    payload={
        "format": "json",
        "record_count": 5,
        "sample": {"day": "Monday", "high": 22, "low": 14},
    },
)
print(f"Evidence submitted: {evidence.id}  verified={evidence.verified}")

# ── 5. Fulfill the promise ──────────────────────────────────────────────────
#    Marking a promise as fulfilled records completion on the ledger.
fulfilled = client.promises.fulfill(promise.id)
print(f"Promise status after fulfillment: {fulfilled.status}")

# ── 6. Check the trust score ────────────────────────────────────────────────
#    Scores are computed from the full history of promises and evidence.
score = client.scores.get(agent_a.id)
print(f"Trust score for {agent_a.name}:")
print(f"  overall  = {score.overall_score}")
print(f"  level    = {score.level}")
print(f"  fulfilled / total = {score.fulfilled_count} / {score.total_promises}")

# ── 7. Clean up ─────────────────────────────────────────────────────────────
client.close()
print("Done.")
