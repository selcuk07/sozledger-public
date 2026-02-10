from __future__ import annotations

from soz_ledger.models import ScoreHistoryResponse, TrustScore
from tests.conftest import SCORE_DATA, SCORE_HISTORY_DATA, make_response


class TestScoresGet:
    def test_sends_get(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, SCORE_DATA)

        client.scores.get("ent_abc123")

        mock_http.request.assert_called_once_with("GET", "/v1/scores/ent_abc123")

    def test_returns_trust_score(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, SCORE_DATA)

        score = client.scores.get("ent_abc123")

        assert isinstance(score, TrustScore)
        assert score.entity_id == "ent_abc123"
        assert score.overall_score == 85.5
        assert score.level == "Reliable"
        assert score.fulfilled_count == 8

    def test_unrated_entity(self, mock_client):
        client, mock_http = mock_client
        unrated = {
            **SCORE_DATA,
            "overall_score": None,
            "level": "Unrated",
            "rated": False,
            "total_promises": 0,
        }
        mock_http.request.return_value = make_response(200, unrated)

        score = client.scores.get("ent_new")

        assert score.overall_score is None
        assert score.rated is False
        assert score.level == "Unrated"


class TestScoresHistory:
    def test_sends_get_to_history_endpoint(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, SCORE_HISTORY_DATA)

        client.scores.history("ent_abc123")

        mock_http.request.assert_called_once_with("GET", "/v1/scores/ent_abc123/history")

    def test_returns_score_history_response(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, SCORE_HISTORY_DATA)

        resp = client.scores.history("ent_abc123")

        assert isinstance(resp, ScoreHistoryResponse)
        assert resp.entity_id == "ent_abc123"
        assert len(resp.history) == 2
        assert resp.history[0].score == 80.0
        assert resp.history[0].level == "Reliable"
        assert resp.history[1].score == 85.5
        assert resp.history[1].timestamp == "2025-01-02T00:00:00Z"
