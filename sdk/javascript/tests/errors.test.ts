import { describe, it, expect } from "vitest";
import { SozLedgerError } from "../src/errors";

describe("SozLedgerError", () => {
  it("stores status, code, and body from API error", () => {
    const body = { error: "not_found", message: "Entity not found" };
    const err = new SozLedgerError(404, body);

    expect(err.status).toBe(404);
    expect(err.code).toBe("not_found");
    expect(err.body).toEqual(body);
    expect(err.message).toBe("Entity not found");
  });

  it("falls back to error field when message is absent", () => {
    const body = { error: "server_error" } as any;
    const err = new SozLedgerError(500, body);

    expect(err.message).toBe("server_error");
    expect(err.code).toBe("server_error");
  });

  it("falls back to HTTP status when no body is provided", () => {
    const err = new SozLedgerError(502);

    expect(err.message).toBe("HTTP 502");
    expect(err.code).toBeUndefined();
    expect(err.body).toBeUndefined();
  });

  it("is an instanceof Error", () => {
    const err = new SozLedgerError(400);
    expect(err).toBeInstanceOf(Error);
    expect(err).toBeInstanceOf(SozLedgerError);
  });

  it("has name set to SozLedgerError", () => {
    const err = new SozLedgerError(400);
    expect(err.name).toBe("SozLedgerError");
  });
});
