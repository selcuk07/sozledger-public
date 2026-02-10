"""
Soz Ledger -- Agent Integration Example
=========================================
Shows how a LangChain-style AI agent can weave Soz Ledger into its
tool-calling loop so that every action is backed by a verifiable promise.
"""

import json
import traceback

from soz_ledger import SozLedgerClient


# ── Simulated LangChain-style agent tool ────────────────────────────────────
def search_web(query: str) -> dict:
    """Placeholder for a real tool call (e.g. SerpAPI, Tavily, etc.)."""
    return {
        "query": query,
        "results": [
            {"title": "Example Result", "url": "https://example.com"},
        ],
    }


def main():
    # ── 1. Initialise the Soz Ledger client ─────────────────────────────────
    client = SozLedgerClient(
        api_key="your_api_key",
        base_url="http://localhost:8000",
    )

    # ── 2. Register the agent entity with platform metadata ─────────────────
    #    Metadata lets you attach non-sensitive context that helps auditors
    #    understand what kind of agent this is.
    agent = client.entities.create(
        name="research-assistant",
        type="ai_agent",
        metadata={
            "framework": "langchain",
            "model": "gpt-4o",
            "version": "0.2.1",
            "owner": "acme-corp",
        },
    )
    print(f"Agent registered: {agent.id}")

    # The "user" or downstream service that the agent is serving.
    user_entity = client.entities.create(
        name="acme-dashboard",
        type="service",
    )

    # ── 3. Create a promise BEFORE doing the work ───────────────────────────
    #    This is the key pattern: declare intent, then execute, then report.
    promise = client.promises.create(
        promisor_id=agent.id,
        promisee_id=user_entity.id,
        description="Search the web and return relevant results for the user query",
        category="task_completion",
    )
    print(f"Promise created: {promise.id}")

    # ── 4. Execute the work inside a try / except ───────────────────────────
    #    On success  -> fulfill the promise
    #    On failure  -> break the promise
    #    In all cases -> submit evidence
    try:
        result = search_web("latest AI safety research papers 2025")

        # Submit evidence of success.
        client.evidence.submit(
            promise_id=promise.id,
            type="output",
            submitted_by=agent.id,
            payload={
                "tool": "search_web",
                "result_count": len(result["results"]),
                "results": result["results"],
            },
        )

        # Mark the promise as fulfilled.
        client.promises.fulfill(promise.id)
        print("Promise fulfilled successfully.")

    except Exception as exc:
        # Submit evidence of failure so the ledger captures *why* it broke.
        client.evidence.submit(
            promise_id=promise.id,
            type="log",
            submitted_by=agent.id,
            payload={
                "error": str(exc),
                "traceback": traceback.format_exc(),
            },
        )

        # Mark the promise as broken.
        client.promises.break_promise(promise.id)
        print(f"Promise broken due to error: {exc}")

    # ── 5. Check the agent's trust score ────────────────────────────────────
    score = client.scores.get(agent.id)
    print(f"\nTrust profile for '{agent.name}':")
    print(f"  Level         : {score.level}")
    print(f"  Overall score : {score.overall_score}")
    print(f"  Fulfilled     : {score.fulfilled_count}")
    print(f"  Broken        : {score.broken_count}")
    print(f"  Streak        : {score.streak}")

    if score.category_scores:
        print("  Category scores:")
        for cat, val in score.category_scores.items():
            print(f"    {cat}: {val}")

    # ── 6. Retrieve score history for trend analysis ────────────────────────
    history = client.scores.history(agent.id)
    print(f"\nScore history entries: {len(history.get('snapshots', []))}")

    client.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
