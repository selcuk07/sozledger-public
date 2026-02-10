from __future__ import annotations

from soz_ledger.models import Entity, TrustScore
from tests.conftest import ENTITY_DATA, SCORE_DATA, make_response


class TestEntitiesCreate:
    def test_sends_post_with_required_fields(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, ENTITY_DATA)

        entity = client.entities.create(name="test-agent", type="agent")

        mock_http.request.assert_called_once_with(
            "POST", "/v1/entities", json={"name": "test-agent", "type": "agent"}
        )

    def test_includes_optional_fields(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, ENTITY_DATA)

        client.entities.create(
            name="test-agent", type="agent", public_key="pk123", metadata={"k": "v"}
        )

        call_kwargs = mock_http.request.call_args
        json_body = call_kwargs.kwargs["json"]
        assert json_body["public_key"] == "pk123"
        assert json_body["metadata"] == {"k": "v"}

    def test_omits_none_optionals(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, ENTITY_DATA)

        client.entities.create(name="a", type="agent")

        json_body = mock_http.request.call_args.kwargs["json"]
        assert "public_key" not in json_body
        assert "metadata" not in json_body

    def test_returns_entity(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, ENTITY_DATA)

        entity = client.entities.create(name="test-agent", type="agent")

        assert isinstance(entity, Entity)
        assert entity.id == "ent_abc123"
        assert entity.name == "test-agent"


class TestEntitiesGet:
    def test_sends_get(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, ENTITY_DATA)

        client.entities.get("ent_abc123")

        mock_http.request.assert_called_once_with("GET", "/v1/entities/ent_abc123")

    def test_returns_entity(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, ENTITY_DATA)

        entity = client.entities.get("ent_abc123")

        assert isinstance(entity, Entity)
        assert entity.id == "ent_abc123"


class TestEntitiesScore:
    def test_returns_trust_score(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, SCORE_DATA)

        score = client.entities.score("ent_abc123")

        mock_http.request.assert_called_once_with("GET", "/v1/entities/ent_abc123/score")
        assert isinstance(score, TrustScore)
        assert score.overall_score == 85.5
