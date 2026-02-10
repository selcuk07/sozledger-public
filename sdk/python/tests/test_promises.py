from __future__ import annotations

from soz_ledger.models import Promise
from tests.conftest import PROMISE_DATA, make_response


class TestPromisesCreate:
    def test_sends_post_with_default_category(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, PROMISE_DATA)

        client.promises.create(
            promisor_id="ent_abc123",
            promisee_id="ent_def456",
            description="Will deliver report",
        )

        json_body = mock_http.request.call_args.kwargs["json"]
        assert json_body["category"] == "custom"
        assert json_body["promisor_id"] == "ent_abc123"

    def test_includes_deadline_when_provided(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, PROMISE_DATA)

        client.promises.create(
            promisor_id="a",
            promisee_id="b",
            description="d",
            deadline="2025-06-01",
        )

        json_body = mock_http.request.call_args.kwargs["json"]
        assert json_body["deadline"] == "2025-06-01"

    def test_omits_none_deadline(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, PROMISE_DATA)

        client.promises.create(promisor_id="a", promisee_id="b", description="d")

        json_body = mock_http.request.call_args.kwargs["json"]
        assert "deadline" not in json_body

    def test_returns_promise(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, PROMISE_DATA)

        p = client.promises.create(promisor_id="a", promisee_id="b", description="d")

        assert isinstance(p, Promise)
        assert p.id == "prm_abc123"
        assert p.status == "active"


class TestPromisesGet:
    def test_sends_get(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, PROMISE_DATA)

        client.promises.get("prm_abc123")

        mock_http.request.assert_called_once_with("GET", "/v1/promises/prm_abc123")

    def test_returns_promise(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, PROMISE_DATA)

        p = client.promises.get("prm_abc123")
        assert isinstance(p, Promise)


class TestPromisesFulfill:
    def test_sends_patch_with_fulfilled_status(self, mock_client):
        client, mock_http = mock_client
        fulfilled = {**PROMISE_DATA, "status": "fulfilled"}
        mock_http.request.return_value = make_response(200, fulfilled)

        p = client.promises.fulfill("prm_abc123")

        mock_http.request.assert_called_once_with(
            "PATCH", "/v1/promises/prm_abc123/status", json={"status": "fulfilled"}
        )
        assert p.status == "fulfilled"


class TestPromisesBreak:
    def test_sends_patch_with_broken_status(self, mock_client):
        client, mock_http = mock_client
        broken = {**PROMISE_DATA, "status": "broken"}
        mock_http.request.return_value = make_response(200, broken)

        p = client.promises.break_promise("prm_abc123")

        mock_http.request.assert_called_once_with(
            "PATCH", "/v1/promises/prm_abc123/status", json={"status": "broken"}
        )
        assert p.status == "broken"


class TestPromisesDispute:
    def test_sends_patch_with_disputed_status(self, mock_client):
        client, mock_http = mock_client
        disputed = {**PROMISE_DATA, "status": "disputed"}
        mock_http.request.return_value = make_response(200, disputed)

        p = client.promises.dispute("prm_abc123")

        mock_http.request.assert_called_once_with(
            "PATCH", "/v1/promises/prm_abc123/status", json={"status": "disputed"}
        )
        assert p.status == "disputed"
