"""Tests for soz_task_callback."""

from unittest.mock import MagicMock

import pytest

from soz_ledger.models import Evidence, Promise
from soz_ledger_crewai.callbacks import soz_task_callback


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.promises.create.return_value = Promise(
        id="promise_001",
        promisor_id="agent_1",
        promisee_id="user_1",
        description="Summarise the document",
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
        description="Summarise the document",
        status="fulfilled",
    )
    return client


class FakeTaskOutput:
    """Mimics CrewAI's TaskOutput without importing crewai."""

    def __init__(self, description: str, agent: str, raw: str):
        self.description = description
        self.agent = agent
        self.raw = raw


class TestSozTaskCallback:
    def test_callback_creates_promise_and_fulfills(self, mock_client):
        callback = soz_task_callback(
            mock_client, agent_entity_id="agent_1", promisee_entity_id="user_1"
        )
        output = FakeTaskOutput(
            description="Summarise the document",
            agent="researcher",
            raw="The document discusses ...",
        )

        callback(output)

        mock_client.promises.create.assert_called_once_with(
            promisor_id="agent_1",
            promisee_id="user_1",
            description="Summarise the document",
            category="custom",
        )
        mock_client.evidence.submit.assert_called_once_with(
            promise_id="promise_001",
            type="output",
            submitted_by="agent_1",
            payload={
                "agent": "researcher",
                "output_preview": "The document discusses ...",
            },
        )
        mock_client.promises.fulfill.assert_called_once_with("promise_001")

    def test_callback_defaults_promisee_to_agent(self, mock_client):
        callback = soz_task_callback(mock_client, agent_entity_id="agent_1")
        output = FakeTaskOutput(
            description="Do something", agent="worker", raw="done"
        )

        callback(output)

        mock_client.promises.create.assert_called_once_with(
            promisor_id="agent_1",
            promisee_id="agent_1",
            description="Do something",
            category="custom",
        )

    def test_callback_truncates_long_output(self, mock_client):
        callback = soz_task_callback(
            mock_client, agent_entity_id="agent_1", promisee_entity_id="user_1"
        )
        output = FakeTaskOutput(
            description="Task", agent="worker", raw="x" * 2000
        )

        callback(output)

        call_payload = mock_client.evidence.submit.call_args.kwargs["payload"]
        assert len(call_payload["output_preview"]) == 1000

    def test_callback_handles_missing_attributes(self, mock_client):
        """TaskOutput-like object with no description/agent/raw attributes."""
        callback = soz_task_callback(
            mock_client, agent_entity_id="agent_1", promisee_entity_id="user_1"
        )

        callback("plain string output")

        mock_client.promises.create.assert_called_once_with(
            promisor_id="agent_1",
            promisee_id="user_1",
            description="CrewAI task completed",
            category="custom",
        )
        mock_client.promises.fulfill.assert_called_once_with("promise_001")
