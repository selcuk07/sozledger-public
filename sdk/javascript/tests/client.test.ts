import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { SozLedgerClient } from "../src/client";
import { SozLedgerError } from "../src/errors";
import {
  mockFetch,
  mockFetchNonJson,
  mockFetchNetworkError,
  ENTITY_FIXTURE,
  ERROR_BODY_FIXTURE,
} from "./helpers";

describe("SozLedgerClient", () => {
  const originalFetch = global.fetch;

  afterEach(() => {
    global.fetch = originalFetch;
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  // ── Constructor ────────────────────────────────────────────────────────

  it("uses default base URL and timeout", () => {
    const client = new SozLedgerClient("key_123");
    // We can verify defaults by making a request and inspecting the URL
    const fn = mockFetch(200, ENTITY_FIXTURE);
    client.entities.get("e1");
    expect(fn).toHaveBeenCalledOnce();
    const url: string = fn.mock.calls[0][0];
    expect(url).toBe("http://localhost:8000/v1/entities/e1");
  });

  it("strips trailing slashes from base URL", () => {
    const client = new SozLedgerClient("key_123", "https://api.example.com///");
    const fn = mockFetch(200, ENTITY_FIXTURE);
    client.entities.get("e1");
    const url: string = fn.mock.calls[0][0];
    expect(url).toBe("https://api.example.com/v1/entities/e1");
  });

  // ── Headers ────────────────────────────────────────────────────────────

  it("sends Authorization Bearer header", async () => {
    const fn = mockFetch(200, ENTITY_FIXTURE);
    const client = new SozLedgerClient("my_secret_key");
    await client.entities.get("e1");

    const init = fn.mock.calls[0][1] as RequestInit;
    expect((init.headers as Record<string, string>)["Authorization"]).toBe(
      "Bearer my_secret_key",
    );
  });

  it("sends Content-Type application/json", async () => {
    const fn = mockFetch(200, ENTITY_FIXTURE);
    const client = new SozLedgerClient("key");
    await client.entities.get("e1");

    const init = fn.mock.calls[0][1] as RequestInit;
    expect((init.headers as Record<string, string>)["Content-Type"]).toBe(
      "application/json",
    );
  });

  // ── Request body ───────────────────────────────────────────────────────

  it("does not send body for GET requests", async () => {
    const fn = mockFetch(200, ENTITY_FIXTURE);
    const client = new SozLedgerClient("key");
    await client.entities.get("e1");

    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("GET");
    expect(init.body).toBeUndefined();
  });

  it("JSON-stringifies body for POST requests", async () => {
    const fn = mockFetch(200, ENTITY_FIXTURE);
    const client = new SozLedgerClient("key");
    await client.entities.create({ name: "a", type: "agent" });

    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("POST");
    expect(JSON.parse(init.body as string)).toEqual({ name: "a", type: "agent" });
  });

  it("JSON-stringifies body for PATCH requests", async () => {
    const fn = mockFetch(200, { ...ENTITY_FIXTURE, status: "fulfilled" });
    const client = new SozLedgerClient("key");
    await client.promises.fulfill("p1");

    const init = fn.mock.calls[0][1] as RequestInit;
    expect(init.method).toBe("PATCH");
    expect(JSON.parse(init.body as string)).toEqual({ status: "fulfilled" });
  });

  // ── Error handling ─────────────────────────────────────────────────────

  it("throws SozLedgerError with parsed body on HTTP error", async () => {
    mockFetch(404, ERROR_BODY_FIXTURE);
    const client = new SozLedgerClient("key");

    await expect(client.entities.get("e1")).rejects.toThrow(SozLedgerError);
    try {
      await client.entities.get("e1");
    } catch (e) {
      const err = e as SozLedgerError;
      expect(err.status).toBe(404);
      expect(err.code).toBe("not_found");
      expect(err.body).toEqual(ERROR_BODY_FIXTURE);
    }
  });

  it("throws SozLedgerError with undefined body on non-JSON error response", async () => {
    mockFetchNonJson(500);
    const client = new SozLedgerClient("key");

    try {
      await client.entities.get("e1");
      expect.unreachable("should have thrown");
    } catch (e) {
      const err = e as SozLedgerError;
      expect(err.status).toBe(500);
      expect(err.body).toBeUndefined();
      expect(err.message).toBe("HTTP 500");
    }
  });

  it("throws SozLedgerError with code 'timeout' on AbortError", async () => {
    vi.useFakeTimers();
    const client = new SozLedgerClient("key", "http://localhost:8000", 100);

    // fetch that never resolves, causing the AbortController to fire
    global.fetch = vi.fn().mockImplementation(
      () => new Promise<Response>((_, reject) => {
        // Listen for abort signal
        const signal = (vi.mocked(global.fetch).mock.calls.at(-1)?.[1] as RequestInit)?.signal;
        signal?.addEventListener("abort", () => {
          const err = new DOMException("The operation was aborted.", "AbortError");
          reject(err);
        });
      }),
    );

    const promise = client.entities.get("e1");
    vi.advanceTimersByTime(150);

    try {
      await promise;
      expect.unreachable("should have thrown");
    } catch (e) {
      const err = e as SozLedgerError;
      expect(err.status).toBe(0);
      expect(err.code).toBe("timeout");
    }

    vi.useRealTimers();
  });

  it("throws SozLedgerError with code 'network_error' on fetch failure", async () => {
    mockFetchNetworkError("DNS resolution failed");
    const client = new SozLedgerClient("key");

    try {
      await client.entities.get("e1");
      expect.unreachable("should have thrown");
    } catch (e) {
      const err = e as SozLedgerError;
      expect(err.status).toBe(0);
      expect(err.code).toBe("network_error");
      expect(err.message).toBe("DNS resolution failed");
    }
  });
});
