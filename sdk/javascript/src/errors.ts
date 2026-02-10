import type { ApiErrorBody } from "./types";

/**
 * Error thrown by the Soz Ledger SDK for HTTP and network failures.
 *
 * - `status` — HTTP status code (`0` for network / timeout errors)
 * - `code`   — Machine-readable error string from the API (e.g. `"not_found"`)
 * - `body`   — Full parsed error response, when available
 */
export class SozLedgerError extends Error {
  public readonly status: number;
  public readonly code: string | undefined;
  public readonly body: ApiErrorBody | undefined;

  constructor(status: number, body?: ApiErrorBody) {
    const msg = body?.message ?? body?.error ?? `HTTP ${status}`;
    super(msg);
    this.name = "SozLedgerError";
    this.status = status;
    this.code = body?.error;
    this.body = body;
  }
}
