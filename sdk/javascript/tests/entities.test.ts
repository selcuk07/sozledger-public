import { describe, it, expect, afterEach } from "vitest";
import { SozLedgerClient } from "../src/client";
import { mockFetch, ENTITY_FIXTURE } from "./helpers";

describe("EntitiesAPI", () => {
  const originalFetch = global.fetch;
  afterEach(() => { global.fetch = originalFetch; });

  it("create() sends POST to /v1/entities with body", async () => {
    const fn = mockFetch(201, ENTITY_FIXTURE);
    const client = new SozLedgerClient("key");

    const result = await client.entities.create({
      name: "test-agent",
      type: "agent",
    });

    expect(fn.mock.calls[0][0]).toContain("/v1/entities");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("POST");
    expect(JSON.parse(init.body as string)).toEqual({
      name: "test-agent",
      type: "agent",
    });
  });

  it("create() returns parsed Entity", async () => {
    mockFetch(201, ENTITY_FIXTURE);
    const client = new SozLedgerClient("key");

    const entity = await client.entities.create({ name: "test-agent", type: "agent" });

    expect(entity.id).toBe("ent_abc123");
    expect(entity.name).toBe("test-agent");
    expect(entity.type).toBe("agent");
    expect(entity.created_at).toBe("2025-01-01T00:00:00Z");
  });

  it("get() sends GET to /v1/entities/:id", async () => {
    const fn = mockFetch(200, ENTITY_FIXTURE);
    const client = new SozLedgerClient("key");

    await client.entities.get("ent_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/entities/ent_abc123");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("GET");
  });

  it("get() returns parsed Entity", async () => {
    mockFetch(200, ENTITY_FIXTURE);
    const client = new SozLedgerClient("key");

    const entity = await client.entities.get("ent_abc123");

    expect(entity.id).toBe("ent_abc123");
    expect(entity.name).toBe("test-agent");
    expect(entity.type).toBe("agent");
  });
});
