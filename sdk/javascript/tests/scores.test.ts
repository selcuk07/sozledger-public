import { describe, it, expect, afterEach } from "vitest";
import { SozLedgerClient } from "../src/client";
import { mockFetch, SCORE_FIXTURE, SCORE_HISTORY_FIXTURE } from "./helpers";

describe("ScoresAPI", () => {
  const originalFetch = global.fetch;
  afterEach(() => { global.fetch = originalFetch; });

  it("get() sends GET to /v1/scores/:entityId", async () => {
    const fn = mockFetch(200, SCORE_FIXTURE);
    const client = new SozLedgerClient("key");

    await client.scores.get("ent_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/scores/ent_abc123");
    expect((fn.mock.calls[0][1] as RequestInit).method).toBe("GET");
  });

  it("get() returns parsed TrustScore", async () => {
    mockFetch(200, SCORE_FIXTURE);
    const client = new SozLedgerClient("key");

    const score = await client.scores.get("ent_abc123");

    expect(score.entity_id).toBe("ent_abc123");
    expect(score.overall_score).toBe(85.5);
    expect(score.level).toBe("Reliable");
    expect(score.rated).toBe(true);
    expect(score.fulfilled_count).toBe(8);
    expect(score.category_scores).toEqual({ delivery: 90, payment: 80 });
    expect(score.streak).toBe(3);
  });

  it("get() handles unrated entity (null score)", async () => {
    const unrated = {
      ...SCORE_FIXTURE,
      overall_score: null,
      level: "Unrated",
      rated: false,
      total_promises: 0,
      fulfilled_count: 0,
      broken_count: 0,
    };
    mockFetch(200, unrated);
    const client = new SozLedgerClient("key");

    const score = await client.scores.get("ent_new");

    expect(score.overall_score).toBeNull();
    expect(score.rated).toBe(false);
    expect(score.level).toBe("Unrated");
  });

  it("history() sends GET to /v1/scores/:entityId/history", async () => {
    const fn = mockFetch(200, SCORE_HISTORY_FIXTURE);
    const client = new SozLedgerClient("key");

    await client.scores.history("ent_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/scores/ent_abc123/history");
    expect((fn.mock.calls[0][1] as RequestInit).method).toBe("GET");
  });

  it("history() returns ScoreHistoryResponse with nested entries", async () => {
    mockFetch(200, SCORE_HISTORY_FIXTURE);
    const client = new SozLedgerClient("key");

    const resp = await client.scores.history("ent_abc123");

    expect(resp.entity_id).toBe("ent_abc123");
    expect(resp.history).toHaveLength(2);
    expect(resp.history[0].score).toBe(80.0);
    expect(resp.history[0].level).toBe("Reliable");
    expect(resp.history[1].score).toBe(85.5);
    expect(resp.history[1].timestamp).toBe("2025-01-02T00:00:00Z");
  });
});
