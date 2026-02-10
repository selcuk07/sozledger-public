// ── Enums / union types ─────────────────────────────────────────────────────

/** The kind of participant in the trust graph. */
export type EntityType = "ai_agent" | "service" | "human" | "organisation";

/** High-level category that a promise belongs to. */
export type PromiseCategory =
  | "data_delivery"
  | "task_completion"
  | "response_time"
  | "accuracy"
  | "privacy"
  | "safety"
  | "custom";

/** Lifecycle status of a promise. */
export type PromiseStatus =
  | "active"
  | "fulfilled"
  | "broken"
  | "disputed"
  | "expired";

/** The kind of evidence attached to a promise. */
export type EvidenceType = "output" | "log" | "attestation" | "metric";

// ── Core interfaces ─────────────────────────────────────────────────────────

/** A participant (agent, service, human, or organisation) in the trust graph. */
export interface Entity {
  id: string;
  name: string;
  type: EntityType;
  public_key?: string | null;
  api_key?: string | null;
  created_at: string;
  metadata?: Record<string, unknown> | null;
}

/** A verifiable commitment from one entity to another. */
export interface Promise {
  id: string;
  promisor_id: string;
  promisee_id: string;
  description: string;
  category: PromiseCategory;
  status: PromiseStatus;
  deadline?: string | null;
  created_at: string;
  fulfilled_at?: string | null;
}

/** An artefact or record submitted as proof for a promise. */
export interface Evidence {
  id: string;
  promise_id: string;
  type: EvidenceType;
  submitted_by: string;
  verified: boolean;
  payload?: Record<string, unknown> | null;
  created_at: string;
  hash: string;
}

/** Computed trust score for an entity. */
export interface TrustScore {
  entity_id: string;
  overall_score: number | null;
  level: string;
  rated: boolean;
  total_promises: number;
  fulfilled_count: number;
  broken_count: number;
  avg_delay_hours: number;
  category_scores?: Record<string, number> | null;
  streak: number;
  score_version: string;
}

// ── Request / option types ──────────────────────────────────────────────────

export interface CreateEntityOptions {
  name: string;
  type: EntityType;
  public_key?: string;
  metadata?: Record<string, unknown>;
}

export interface CreatePromiseOptions {
  promisor_id: string;
  promisee_id: string;
  description: string;
  category?: PromiseCategory;
  deadline?: string;
}

export interface SubmitEvidenceOptions {
  type: EvidenceType;
  submitted_by: string;
  payload?: Record<string, unknown>;
}

export interface ScoreHistoryResponse {
  entity_id: string;
  snapshots: Array<{
    timestamp: string;
    overall_score: number | null;
    level: string;
  }>;
}
