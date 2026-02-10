from dataclasses import dataclass, field
from typing import Any


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
