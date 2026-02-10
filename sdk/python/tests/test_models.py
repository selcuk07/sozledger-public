from __future__ import annotations

from soz_ledger.models import (
    Entity,
    Evidence,
    Promise,
    ScoreHistoryEntry,
    ScoreHistoryResponse,
    TrustScore,
    _from_dict,
)


class TestFromDict:
    def test_creates_entity_from_full_dict(self):
        data = {
            "id": "ent_1",
            "name": "agent",
            "type": "agent",
            "public_key": "pk",
            "api_key": "ak",
            "created_at": "2025-01-01",
            "metadata": {"k": "v"},
        }
        e = _from_dict(Entity, data)
        assert e.id == "ent_1"
        assert e.name == "agent"
        assert e.metadata == {"k": "v"}

    def test_ignores_unknown_fields(self):
        data = {"id": "ent_1", "name": "agent", "type": "agent", "unknown_field": 42}
        e = _from_dict(Entity, data)
        assert e.id == "ent_1"
        assert not hasattr(e, "unknown_field")

    def test_uses_defaults_for_missing_optional_fields(self):
        data = {"id": "ent_1", "name": "agent", "type": "agent"}
        e = _from_dict(Entity, data)
        assert e.public_key is None
        assert e.api_key is None
        assert e.created_at == ""
        assert e.metadata is None


class TestEntity:
    def test_minimal_construction(self):
        e = Entity(id="1", name="a", type="agent")
        assert e.id == "1"
        assert e.public_key is None


class TestPromise:
    def test_defaults(self):
        p = Promise(id="1", promisor_id="a", promisee_id="b", description="d")
        assert p.category == "custom"
        assert p.status == "active"
        assert p.deadline is None

    def test_from_dict_with_all_fields(self):
        data = {
            "id": "prm_1",
            "promisor_id": "a",
            "promisee_id": "b",
            "description": "d",
            "category": "delivery",
            "status": "fulfilled",
            "deadline": "2025-06-01",
            "created_at": "2025-01-01",
            "fulfilled_at": "2025-02-01",
        }
        p = _from_dict(Promise, data)
        assert p.status == "fulfilled"
        assert p.fulfilled_at == "2025-02-01"


class TestEvidence:
    def test_defaults(self):
        e = Evidence(id="1", promise_id="p", type="manual", submitted_by="a")
        assert e.verified is False
        assert e.payload is None
        assert e.hash == ""


class TestTrustScore:
    def test_defaults(self):
        s = TrustScore(entity_id="e1")
        assert s.overall_score is None
        assert s.level == "Unrated"
        assert s.rated is False
        assert s.streak == 0

    def test_from_dict_with_full_data(self):
        data = {
            "entity_id": "e1",
            "overall_score": 90.0,
            "level": "Trusted",
            "rated": True,
            "total_promises": 5,
            "fulfilled_count": 5,
            "broken_count": 0,
            "avg_delay_hours": 0.0,
            "category_scores": {"delivery": 100},
            "streak": 5,
            "score_version": "v1",
            "last_updated": "2025-01-01",
        }
        s = _from_dict(TrustScore, data)
        assert s.overall_score == 90.0
        assert s.category_scores == {"delivery": 100}


class TestScoreHistoryResponse:
    def test_construction_with_entries(self):
        entries = [
            ScoreHistoryEntry(score=80.0, level="Reliable", timestamp="2025-01-01"),
            ScoreHistoryEntry(score=90.0, level="Trusted", timestamp="2025-02-01"),
        ]
        resp = ScoreHistoryResponse(entity_id="e1", history=entries)
        assert resp.entity_id == "e1"
        assert len(resp.history) == 2
        assert resp.history[0].score == 80.0
        assert resp.history[1].level == "Trusted"

    def test_default_empty_history(self):
        resp = ScoreHistoryResponse(entity_id="e1")
        assert resp.history == []
