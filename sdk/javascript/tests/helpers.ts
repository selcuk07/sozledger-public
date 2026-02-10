import { vi } from "vitest";

// ── Fixture data ────────────────────────────────────────────────────────────

export const ENTITY_FIXTURE = {
  id: "ent_abc123",
  name: "test-agent",
  type: "agent" as const,
  public_key: null,
  api_key: "sk_test_key",
  created_at: "2025-01-01T00:00:00Z",
  metadata: null,
};

export const PROMISE_FIXTURE = {
  id: "prm_abc123",
  promisor_id: "ent_abc123",
  promisee_id: "ent_def456",
  description: "Will deliver report",
  category: "delivery" as const,
  status: "active" as const,
  deadline: "2025-06-01T00:00:00Z",
  created_at: "2025-01-01T00:00:00Z",
  fulfilled_at: null,
};

export const EVIDENCE_FIXTURE = {
  id: "ev_abc123",
  promise_id: "prm_abc123",
  type: "manual" as const,
  submitted_by: "ent_abc123",
  verified: false,
  payload: { note: "Delivered via email" },
  created_at: "2025-01-02T00:00:00Z",
  hash: "sha256_abc",
};

export const SCORE_FIXTURE = {
  entity_id: "ent_abc123",
  entity_name: "test-agent",
  overall_score: 85.5,
  level: "Reliable",
  rated: true,
  total_promises: 10,
  fulfilled_count: 8,
  broken_count: 1,
  avg_delay_hours: 2.5,
  category_scores: { delivery: 90, payment: 80 },
  streak: 3,
  score_version: "v1",
  last_updated: "2025-01-03T00:00:00Z",
};

export const SCORE_HISTORY_FIXTURE = {
  entity_id: "ent_abc123",
  history: [
    { score: 80.0, level: "Reliable", timestamp: "2025-01-01T00:00:00Z", version: "v1" },
    { score: 85.5, level: "Reliable", timestamp: "2025-01-02T00:00:00Z", version: "v1" },
  ],
};

export const ERROR_BODY_FIXTURE = {
  error: "not_found",
  message: "Entity not found",
};

// ── Mock helpers ────────────────────────────────────────────────────────────

/**
 * Build a mock Response object that behaves like fetch's Response.
 */
export function mockResponse(status: number, body: unknown): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(body),
    headers: new Headers({ "content-type": "application/json" }),
  } as unknown as Response;
}

/**
 * Install a mock `global.fetch` that resolves with the given status and body.
 * Returns the mock function so callers can inspect calls.
 */
export function mockFetch(status: number, body: unknown) {
  const fn = vi.fn().mockResolvedValue(mockResponse(status, body));
  global.fetch = fn;
  return fn;
}

/**
 * Install a mock `global.fetch` whose `.json()` throws (non-JSON response).
 */
export function mockFetchNonJson(status: number) {
  const fn = vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.reject(new SyntaxError("Unexpected token")),
    headers: new Headers(),
  } as unknown as Response);
  global.fetch = fn;
  return fn;
}

/**
 * Install a mock `global.fetch` that rejects with a network error.
 */
export function mockFetchNetworkError(message = "Failed to fetch") {
  const err = new TypeError(message);
  const fn = vi.fn().mockRejectedValue(err);
  global.fetch = fn;
  return fn;
}
