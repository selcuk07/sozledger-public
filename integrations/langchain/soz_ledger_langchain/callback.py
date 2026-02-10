"""Soz Ledger callback handler for LangChain.

Automatically wraps every tool call as a Soz Ledger promise:
  - on_tool_start  -> creates a promise
  - on_tool_end    -> submits evidence + fulfills
  - on_tool_error  -> submits evidence + breaks
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler

from soz_ledger import SozLedgerClient
from soz_ledger.models import Promise


class SozLedgerCallbackHandler(BaseCallbackHandler):
    """LangChain callback handler that records tool calls as Soz Ledger promises.

    Usage::

        handler = SozLedgerCallbackHandler(client, agent_entity_id="ent_abc")
        agent.invoke({"input": "..."}, config={"callbacks": [handler]})
    """

    def __init__(
        self,
        client: SozLedgerClient,
        agent_entity_id: str,
        promisee_entity_id: str | None = None,
    ) -> None:
        super().__init__()
        self.client = client
        self.agent_entity_id = agent_entity_id
        self.promisee_entity_id = promisee_entity_id or agent_entity_id
        self._promises: dict[UUID, Promise] = {}

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        """Create a promise when a tool invocation begins."""
        tool_name = serialized.get("name", "unknown_tool")
        description = f"Tool call: {tool_name}"

        promise = self.client.promises.create(
            promisor_id=self.agent_entity_id,
            promisee_id=self.promisee_entity_id,
            description=description,
            category="custom",
        )
        self._promises[run_id] = promise

    def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        """Submit evidence and fulfill the promise when a tool succeeds."""
        promise = self._promises.pop(run_id, None)
        if promise is None:
            return

        preview = output[:1000] if isinstance(output, str) else str(output)[:1000]

        self.client.evidence.submit(
            promise_id=promise.id,
            type="output",
            submitted_by=self.agent_entity_id,
            payload={"output_preview": preview},
        )
        self.client.promises.fulfill(promise.id)

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        """Submit evidence and break the promise when a tool fails."""
        promise = self._promises.pop(run_id, None)
        if promise is None:
            return

        self.client.evidence.submit(
            promise_id=promise.id,
            type="log",
            submitted_by=self.agent_entity_id,
            payload={"error": str(error)[:1000]},
        )
        self.client.promises.break_promise(promise.id)
