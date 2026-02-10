"""Tests for SozLedgerCallbackHandler."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from soz_ledger.models import Evidence, Promise
from soz_ledger_langchain.callback import SozLedgerCallbackHandler


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.promises.create.return_value = Promise(
        id="promise_001",
        promisor_id="agent_1",
        promisee_id="user_1",
        description="Tool call: search",
    )
    client.evidence.submit.return_value = Evidence(
        id="ev_001",
        promise_id="promise_001",
        type="output",
        submitted_by="agent_1",
    )
    client.promises.fulfill.return_value = Promise(
        id="promise_001",
        promisor_id="agent_1",
        promisee_id="user_1",
        description="Tool call: search",
        status="fulfilled",
    )
    client.promises.break_promise.return_value = Promise(
        id="promise_001",
        promisor_id="agent_1",
        promisee_id="user_1",
        description="Tool call: search",
        status="broken",
    )
    return client


@pytest.fixture
def handler(mock_client):
    return SozLedgerCallbackHandler(
        client=mock_client,
        agent_entity_id="agent_1",
        promisee_entity_id="user_1",
    )


class TestToolStartEnd:
    """Tool start -> tool end lifecycle."""

    def test_tool_start_creates_promise(self, handler, mock_client):
        run_id = uuid4()
        handler.on_tool_start(
            serialized={"name": "search"},
            input_str="query text",
            run_id=run_id,
        )

        mock_client.promises.create.assert_called_once_with(
            promisor_id="agent_1",
            promisee_id="user_1",
            description="Tool call: search",
            category="custom",
        )
        assert run_id in handler._promises

    def test_tool_end_fulfills_promise(self, handler, mock_client):
        run_id = uuid4()
        handler.on_tool_start(
            serialized={"name": "search"},
            input_str="query",
            run_id=run_id,
        )

        handler.on_tool_end(output="result data", run_id=run_id)

        mock_client.evidence.submit.assert_called_once_with(
            promise_id="promise_001",
            type="output",
            submitted_by="agent_1",
            payload={"output_preview": "result data"},
        )
        mock_client.promises.fulfill.assert_called_once_with("promise_001")
        assert run_id not in handler._promises

    def test_tool_end_truncates_long_output(self, handler, mock_client):
        run_id = uuid4()
        handler.on_tool_start(
            serialized={"name": "search"},
            input_str="query",
            run_id=run_id,
        )

        long_output = "x" * 2000
        handler.on_tool_end(output=long_output, run_id=run_id)

        call_payload = mock_client.evidence.submit.call_args.kwargs["payload"]
        assert len(call_payload["output_preview"]) == 1000


class TestToolStartError:
    """Tool start -> tool error lifecycle."""

    def test_tool_error_breaks_promise(self, handler, mock_client):
        run_id = uuid4()
        handler.on_tool_start(
            serialized={"name": "search"},
            input_str="query",
            run_id=run_id,
        )

        handler.on_tool_error(error=RuntimeError("connection failed"), run_id=run_id)

        mock_client.evidence.submit.assert_called_once_with(
            promise_id="promise_001",
            type="log",
            submitted_by="agent_1",
            payload={"error": "connection failed"},
        )
        mock_client.promises.break_promise.assert_called_once_with("promise_001")
        assert run_id not in handler._promises


class TestDefensiveBehavior:
    """Edge cases that should not crash."""

    def test_tool_end_without_start_is_noop(self, handler, mock_client):
        handler.on_tool_end(output="result", run_id=uuid4())

        mock_client.evidence.submit.assert_not_called()
        mock_client.promises.fulfill.assert_not_called()

    def test_tool_error_without_start_is_noop(self, handler, mock_client):
        handler.on_tool_error(error=RuntimeError("fail"), run_id=uuid4())

        mock_client.evidence.submit.assert_not_called()
        mock_client.promises.break_promise.assert_not_called()
