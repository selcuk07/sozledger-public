from __future__ import annotations

from soz_ledger.models import Evidence
from tests.conftest import EVIDENCE_DATA, make_response


class TestEvidenceSubmit:
    def test_sends_post_with_required_fields(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, EVIDENCE_DATA)

        client.evidence.submit(
            promise_id="prm_abc123",
            type="manual",
            submitted_by="ent_abc123",
        )

        mock_http.request.assert_called_once_with(
            "POST",
            "/v1/promises/prm_abc123/evidence",
            json={"type": "manual", "submitted_by": "ent_abc123"},
        )

    def test_includes_payload_when_provided(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, EVIDENCE_DATA)

        client.evidence.submit(
            promise_id="prm_abc123",
            type="manual",
            submitted_by="ent_abc123",
            payload={"note": "done"},
        )

        json_body = mock_http.request.call_args.kwargs["json"]
        assert json_body["payload"] == {"note": "done"}

    def test_omits_none_payload(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, EVIDENCE_DATA)

        client.evidence.submit(
            promise_id="prm_abc123", type="manual", submitted_by="ent_abc123"
        )

        json_body = mock_http.request.call_args.kwargs["json"]
        assert "payload" not in json_body

    def test_returns_evidence(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, EVIDENCE_DATA)

        ev = client.evidence.submit(
            promise_id="prm_abc123", type="manual", submitted_by="ent_abc123"
        )

        assert isinstance(ev, Evidence)
        assert ev.id == "ev_abc123"
        assert ev.hash == "sha256_abc"


class TestEvidenceList:
    def test_returns_list_of_evidence(self, mock_client):
        client, mock_http = mock_client
        second = {**EVIDENCE_DATA, "id": "ev_def456"}
        mock_http.request.return_value = make_response(200, [EVIDENCE_DATA, second])

        result = client.evidence.list("prm_abc123")

        mock_http.request.assert_called_once_with(
            "GET", "/v1/promises/prm_abc123/evidence"
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(e, Evidence) for e in result)
        assert result[0].id == "ev_abc123"
        assert result[1].id == "ev_def456"
