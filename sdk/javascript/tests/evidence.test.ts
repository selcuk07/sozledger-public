import { describe, it, expect, afterEach } from "vitest";
import { SozLedgerClient } from "../src/client";
import { mockFetch, EVIDENCE_FIXTURE } from "./helpers";

describe("EvidenceAPI", () => {
  const originalFetch = global.fetch;
  afterEach(() => { global.fetch = originalFetch; });

  it("submit() sends POST to /v1/promises/:id/evidence", async () => {
    const fn = mockFetch(201, EVIDENCE_FIXTURE);
    const client = new SozLedgerClient("key");

    await client.evidence.submit("prm_abc123", {
      type: "manual",
      submitted_by: "ent_abc123",
      payload: { note: "Delivered via email" },
    });

    expect(fn.mock.calls[0][0]).toContain("/v1/promises/prm_abc123/evidence");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("POST");
    const body = JSON.parse(init.body as string);
    expect(body.type).toBe("manual");
    expect(body.submitted_by).toBe("ent_abc123");
    expect(body.payload).toEqual({ note: "Delivered via email" });
  });

  it("submit() returns parsed Evidence", async () => {
    mockFetch(201, EVIDENCE_FIXTURE);
    const client = new SozLedgerClient("key");

    const ev = await client.evidence.submit("prm_abc123", {
      type: "manual",
      submitted_by: "ent_abc123",
    });

    expect(ev.id).toBe("ev_abc123");
    expect(ev.promise_id).toBe("prm_abc123");
    expect(ev.verified).toBe(false);
    expect(ev.hash).toBe("sha256_abc");
  });

  it("list() sends GET to /v1/promises/:id/evidence", async () => {
    const fn = mockFetch(200, [EVIDENCE_FIXTURE]);
    const client = new SozLedgerClient("key");

    await client.evidence.list("prm_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/promises/prm_abc123/evidence");
    expect((fn.mock.calls[0][1] as RequestInit).method).toBe("GET");
  });

  it("list() returns array of Evidence", async () => {
    const second = { ...EVIDENCE_FIXTURE, id: "ev_def456" };
    mockFetch(200, [EVIDENCE_FIXTURE, second]);
    const client = new SozLedgerClient("key");

    const list = await client.evidence.list("prm_abc123");

    expect(Array.isArray(list)).toBe(true);
    expect(list).toHaveLength(2);
    expect(list[0].id).toBe("ev_abc123");
    expect(list[1].id).toBe("ev_def456");
  });
});
