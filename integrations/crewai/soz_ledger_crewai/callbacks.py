"""Soz Ledger callback factory for CrewAI.

Provides a factory function that returns a task callback compatible with
CrewAI's ``Task(callback=...)`` parameter. Each completed task is automatically
recorded as a fulfilled promise on the Soz Ledger trust protocol.
"""

from __future__ import annotations

from typing import Any, Callable

from soz_ledger import SozLedgerClient


def soz_task_callback(
    client: SozLedgerClient,
    agent_entity_id: str,
    promisee_entity_id: str | None = None,
) -> Callable[[Any], None]:
    """Create a CrewAI task callback that records completed tasks as promises.

    Usage::

        from crewai import Task
        from soz_ledger_crewai import soz_task_callback

        callback = soz_task_callback(client, agent_entity_id="ent_abc")
        task = Task(description="...", callback=callback)

    Args:
        client: An initialised SozLedgerClient.
        agent_entity_id: The entity ID of the agent making promises.
        promisee_entity_id: The entity receiving the promise. Defaults to
            agent_entity_id if not provided.

    Returns:
        A callback function compatible with CrewAI's Task(callback=...).
    """
    promisee_id = promisee_entity_id or agent_entity_id

    def callback(output: Any) -> None:
        # Extract useful fields from CrewAI's TaskOutput
        description = getattr(output, "description", None) or "CrewAI task completed"
        agent_name = getattr(output, "agent", None) or "unknown_agent"
        raw_output = getattr(output, "raw", None) or str(output)

        preview = str(raw_output)[:1000]

        promise = client.promises.create(
            promisor_id=agent_entity_id,
            promisee_id=promisee_id,
            description=description,
            category="custom",
        )

        client.evidence.submit(
            promise_id=promise.id,
            type="output",
            submitted_by=agent_entity_id,
            payload={
                "agent": str(agent_name),
                "output_preview": preview,
            },
        )

        client.promises.fulfill(promise.id)

    return callback
