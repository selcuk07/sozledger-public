from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from soz_ledger.client import SozLedgerClient


# ── Fixture data ─────────────────────────────────────────────────────────────

ENTITY_DATA = {
    "id": "ent_abc123",
    "name": "test-agent",
    "type": "agent",
    "public_key": None,
    "api_key": "sk_test_key",
    "created_at": "2025-01-01T00:00:00Z",
    "metadata": None,
}

PROMISE_DATA = {
    "id": "prm_abc123",
    "promisor_id": "ent_abc123",
    "promisee_id": "ent_def456",
    "description": "Will deliver report",
    "category": "delivery",
    "status": "active",
    "deadline": "2025-06-01T00:00:00Z",
    "created_at": "2025-01-01T00:00:00Z",
    "fulfilled_at": None,
}

EVIDENCE_DATA = {
    "id": "ev_abc123",
    "promise_id": "prm_abc123",
    "type": "manual",
    "submitted_by": "ent_abc123",
    "verified": False,
    "payload": {"note": "Delivered via email"},
    "created_at": "2025-01-02T00:00:00Z",
    "hash": "sha256_abc",
}

SCORE_DATA = {
    "entity_id": "ent_abc123",
    "entity_name": "test-agent",
    "overall_score": 85.5,
    "level": "Reliable",
    "rated": True,
    "total_promises": 10,
    "fulfilled_count": 8,
    "broken_count": 1,
    "avg_delay_hours": 2.5,
    "category_scores": {"delivery": 90, "payment": 80},
    "streak": 3,
    "score_version": "v1",
    "last_updated": "2025-01-03T00:00:00Z",
}

SCORE_HISTORY_DATA = {
    "entity_id": "ent_abc123",
    "history": [
        {"score": 80.0, "level": "Reliable", "timestamp": "2025-01-01T00:00:00Z", "version": "v1"},
        {"score": 85.5, "level": "Reliable", "timestamp": "2025-01-02T00:00:00Z", "version": "v1"},
    ],
}

ERROR_BODY = {
    "error": "not_found",
    "message": "Entity not found",
}


# ── Helpers ──────────────────────────────────────────────────────────────────


def make_response(status_code: int, json_data=None):
    """Build a mock httpx.Response with .is_success, .status_code, .json()."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.is_success = 200 <= status_code < 300
    if json_data is not None:
        resp.json.return_value = json_data
    else:
        resp.json.side_effect = Exception("No JSON body")
    return resp


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture()
def mock_client():
    """Return (client, mock_http) where mock_http is the patched httpx.Client."""
    with patch("soz_ledger.client.httpx.Client") as MockHttpClass:
        mock_http = MagicMock()
        MockHttpClass.return_value = mock_http
        client = SozLedgerClient("test_api_key")
        yield client, mock_http
