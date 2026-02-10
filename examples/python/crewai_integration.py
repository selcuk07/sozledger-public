"""
Soz Ledger -- CrewAI Integration Example
==========================================
Shows how to use soz_task_callback with CrewAI so that every completed task
is automatically recorded as a verifiable promise.

Requirements:
    pip install soz-ledger soz-ledger-crewai crewai
"""

from crewai import Agent, Crew, Task

from soz_ledger import SozLedgerClient
from soz_ledger_crewai import soz_task_callback


def main():
    # ── 1. Set up Soz Ledger ─────────────────────────────────────────────────
    client = SozLedgerClient(
        api_key="your_api_key",
        base_url="https://api-production-c4c8.up.railway.app",
    )

    # Register the agent entity
    agent_entity = client.entities.create(
        name="crewai-researcher",
        type="agent",
        metadata={"framework": "crewai", "role": "researcher"},
    )

    # ── 2. Create the task callback ──────────────────────────────────────────
    callback = soz_task_callback(
        client=client,
        agent_entity_id=agent_entity.id,
    )

    # ── 3. Define CrewAI agents and tasks ─────────────────────────────────────
    researcher = Agent(
        role="Researcher",
        goal="Find accurate information about AI trust protocols",
        backstory="You are an expert AI researcher.",
    )

    task = Task(
        description="Research the current state of AI agent trust protocols",
        expected_output="A brief summary of AI trust protocol approaches",
        agent=researcher,
        callback=callback,  # <-- Soz Ledger records this on completion
    )

    # ── 4. Run the crew ───────────────────────────────────────────────────────
    crew = Crew(agents=[researcher], tasks=[task])
    result = crew.kickoff()
    print(f"Crew output: {result}")

    # ── 5. Check trust score ──────────────────────────────────────────────────
    score = client.scores.get(agent_entity.id)
    print(f"\nTrust profile for '{agent_entity.name}':")
    print(f"  Level         : {score.level}")
    print(f"  Overall score : {score.overall_score}")
    print(f"  Fulfilled     : {score.fulfilled_count}")
    print(f"  Broken        : {score.broken_count}")

    client.close()


if __name__ == "__main__":
    main()
