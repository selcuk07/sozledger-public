import { describe, it, expect, afterEach } from "vitest";
import { SozLedgerClient } from "../src/client";
import { mockFetch, PROMISE_FIXTURE } from "./helpers";

describe("PromisesAPI", () => {
  const originalFetch = global.fetch;
  afterEach(() => { global.fetch = originalFetch; });

  it("create() sends POST to /v1/promises", async () => {
    const fn = mockFetch(201, PROMISE_FIXTURE);
    const client = new SozLedgerClient("key");

    await client.promises.create({
      promisor_id: "ent_abc123",
      promisee_id: "ent_def456",
      description: "Will deliver report",
    });

    expect(fn.mock.calls[0][0]).toContain("/v1/promises");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("POST");
    const body = JSON.parse(init.body as string);
    expect(body.promisor_id).toBe("ent_abc123");
    expect(body.promisee_id).toBe("ent_def456");
    expect(body.description).toBe("Will deliver report");
  });

  it("create() returns parsed Promise", async () => {
    mockFetch(201, PROMISE_FIXTURE);
    const client = new SozLedgerClient("key");

    const p = await client.promises.create({
      promisor_id: "ent_abc123",
      promisee_id: "ent_def456",
      description: "Will deliver report",
    });

    expect(p.id).toBe("prm_abc123");
    expect(p.status).toBe("active");
    expect(p.category).toBe("delivery");
  });

  it("get() sends GET to /v1/promises/:id", async () => {
    const fn = mockFetch(200, PROMISE_FIXTURE);
    const client = new SozLedgerClient("key");

    await client.promises.get("prm_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/promises/prm_abc123");
    expect((fn.mock.calls[0][1] as RequestInit).method).toBe("GET");
  });

  it("get() returns parsed Promise", async () => {
    mockFetch(200, PROMISE_FIXTURE);
    const client = new SozLedgerClient("key");

    const p = await client.promises.get("prm_abc123");
    expect(p.id).toBe("prm_abc123");
    expect(p.promisor_id).toBe("ent_abc123");
  });

  it("fulfill() sends PATCH with status fulfilled", async () => {
    const fulfilled = { ...PROMISE_FIXTURE, status: "fulfilled", fulfilled_at: "2025-02-01T00:00:00Z" };
    const fn = mockFetch(200, fulfilled);
    const client = new SozLedgerClient("key");

    const p = await client.promises.fulfill("prm_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/promises/prm_abc123/status");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("PATCH");
    expect(JSON.parse(init.body as string)).toEqual({ status: "fulfilled" });
    expect(p.status).toBe("fulfilled");
  });

  it("breakPromise() sends PATCH with status broken", async () => {
    const broken = { ...PROMISE_FIXTURE, status: "broken" };
    const fn = mockFetch(200, broken);
    const client = new SozLedgerClient("key");

    const p = await client.promises.breakPromise("prm_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/promises/prm_abc123/status");
    expect(JSON.parse((fn.mock.calls[0][1] as RequestInit).body as string)).toEqual({ status: "broken" });
    expect(p.status).toBe("broken");
  });

  it("dispute() sends PATCH with status disputed", async () => {
    const disputed = { ...PROMISE_FIXTURE, status: "disputed" };
    const fn = mockFetch(200, disputed);
    const client = new SozLedgerClient("key");

    const p = await client.promises.dispute("prm_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/promises/prm_abc123/status");
    expect(JSON.parse((fn.mock.calls[0][1] as RequestInit).body as string)).toEqual({ status: "disputed" });
    expect(p.status).toBe("disputed");
  });

  it("dispute() returns parsed Promise response", async () => {
    const disputed = { ...PROMISE_FIXTURE, status: "disputed" };
    mockFetch(200, disputed);
    const client = new SozLedgerClient("key");

    const p = await client.promises.dispute("prm_abc123");
    expect(p.id).toBe("prm_abc123");
    expect(p.status).toBe("disputed");
    expect(p.promisor_id).toBe("ent_abc123");
  });
});
