from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any


def _from_dict(cls: type, data: dict[str, Any]):
    """Construct a dataclass instance, silently ignoring unknown fields."""
    known = {f.name for f in dataclasses.fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class Entity:
    id: str
    name: str
    type: str
    public_key: str | None = None
    api_key: str | None = None
    created_at: str = ""
    metadata: dict | None = None


@dataclass
class Promise:
    id: str
    promisor_id: str
    promisee_id: str
    description: str
    category: str = "custom"
    status: str = "active"
    deadline: str | None = None
    created_at: str = ""
    fulfilled_at: str | None = None


@dataclass
class Evidence:
    id: str
    promise_id: str
    type: str
    submitted_by: str
    verified: bool = False
    payload: dict | None = None
    created_at: str = ""
    hash: str = ""


@dataclass
class TrustScore:
    entity_id: str
    entity_name: str | None = None
    overall_score: float | None = None
    level: str = "Unrated"
    rated: bool = False
    total_promises: int = 0
    fulfilled_count: int = 0
    broken_count: int = 0
    avg_delay_hours: float = 0.0
    category_scores: dict | None = None
    streak: int = 0
    score_version: str = "v1"
    last_updated: str | None = None


@dataclass
class ScoreHistoryEntry:
    score: float | None
    level: str
    timestamp: str | None = None
    version: str = "v1"


@dataclass
class ScoreHistoryResponse:
    entity_id: str
    history: list[ScoreHistoryEntry] = field(default_factory=list)


@dataclass
class Webhook:
    id: str
    entity_id: str
    url: str
    event_types: list[str] = field(default_factory=list)
    is_active: bool = True
    created_at: str = ""
    updated_at: str = ""


@dataclass
class WebhookWithSecret(Webhook):
    secret: str = ""


@dataclass
class DeliveryLog:
    id: str
    webhook_id: str
    event_id: str
    event_type: str
    attempt_number: int = 1
    status_code: int | None = None
    response_body: str | None = None
    success: bool = False
    error_message: str | None = None
    next_retry_at: str | None = None
    created_at: str = ""
