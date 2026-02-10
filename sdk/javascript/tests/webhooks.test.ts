import { describe, it, expect, afterEach } from "vitest";
import { SozLedgerClient } from "../src/client";
import {
  mockFetch,
  mockResponse,
  WEBHOOK_FIXTURE,
  WEBHOOK_WITH_SECRET_FIXTURE,
  DELIVERY_LOG_FIXTURE,
} from "./helpers";

describe("WebhooksAPI", () => {
  const originalFetch = global.fetch;
  afterEach(() => { global.fetch = originalFetch; });

  it("create() sends POST to /v1/webhooks with body", async () => {
    const fn = mockFetch(201, WEBHOOK_WITH_SECRET_FIXTURE);
    const client = new SozLedgerClient("key");

    const result = await client.webhooks.create({
      url: "https://example.com/webhook",
      event_types: ["promise.created", "promise.fulfilled"],
    });

    expect(fn.mock.calls[0][0]).toContain("/v1/webhooks");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("POST");
    expect(JSON.parse(init.body as string)).toEqual({
      url: "https://example.com/webhook",
      event_types: ["promise.created", "promise.fulfilled"],
    });
    expect(result.secret).toBe("whsec_test_secret_123");
  });

  it("list() sends GET to /v1/webhooks", async () => {
    const fn = mockFetch(200, [WEBHOOK_FIXTURE]);
    const client = new SozLedgerClient("key");

    const result = await client.webhooks.list();

    expect(fn.mock.calls[0][0]).toContain("/v1/webhooks");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("GET");
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe("wh_abc123");
  });

  it("get() sends GET to /v1/webhooks/:id", async () => {
    const fn = mockFetch(200, WEBHOOK_FIXTURE);
    const client = new SozLedgerClient("key");

    const result = await client.webhooks.get("wh_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/webhooks/wh_abc123");
    expect(result.url).toBe("https://example.com/webhook");
  });

  it("update() sends PATCH to /v1/webhooks/:id", async () => {
    const fn = mockFetch(200, WEBHOOK_FIXTURE);
    const client = new SozLedgerClient("key");

    const result = await client.webhooks.update("wh_abc123", { is_active: false });

    expect(fn.mock.calls[0][0]).toContain("/v1/webhooks/wh_abc123");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("PATCH");
    expect(JSON.parse(init.body as string)).toEqual({ is_active: false });
    expect(result.id).toBe("wh_abc123");
  });

  it("delete() sends DELETE to /v1/webhooks/:id", async () => {
    const fn = mockFetch(204, null);
    const client = new SozLedgerClient("key");

    await client.webhooks.delete("wh_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/webhooks/wh_abc123");
    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("DELETE");
  });

  it("logs() sends GET to /v1/webhooks/:id/logs", async () => {
    const fn = mockFetch(200, [DELIVERY_LOG_FIXTURE]);
    const client = new SozLedgerClient("key");

    const result = await client.webhooks.logs("wh_abc123");

    expect(fn.mock.calls[0][0]).toContain("/v1/webhooks/wh_abc123/logs");
    expect(result).toHaveLength(1);
    expect(result[0].success).toBe(true);
    expect(result[0].event_type).toBe("promise.created");
  });
});
