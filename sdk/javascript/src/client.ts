import type {
  ApiErrorBody,
  CreateEntityOptions,
  CreatePromiseOptions,
  Entity,
  Evidence,
  Promise as SozPromise,
  ScoreHistoryResponse,
  SubmitEvidenceOptions,
  TrustScore,
} from "./types";
import { SozLedgerError } from "./errors";

// ── Sub-API classes ─────────────────────────────────────────────────────────

class EntitiesAPI {
  constructor(private client: SozLedgerClient) {}

  /** Register a new entity in the trust graph. */
  async create(options: CreateEntityOptions): Promise<Entity> {
    return this.client._post<Entity>("/v1/entities", options);
  }

  /** Retrieve an entity by ID. */
  async get(entityId: string): Promise<Entity> {
    return this.client._get<Entity>(`/v1/entities/${entityId}`);
  }
}

class PromisesAPI {
  constructor(private client: SozLedgerClient) {}

  /** Create a new promise between two entities. */
  async create(options: CreatePromiseOptions): Promise<SozPromise> {
    return this.client._post<SozPromise>("/v1/promises", options);
  }

  /** Retrieve a promise by ID. */
  async get(promiseId: string): Promise<SozPromise> {
    return this.client._get<SozPromise>(`/v1/promises/${promiseId}`);
  }

  /** Mark a promise as fulfilled. */
  async fulfill(promiseId: string): Promise<SozPromise> {
    return this.client._patch<SozPromise>(
      `/v1/promises/${promiseId}/status`,
      { status: "fulfilled" },
    );
  }

  /** Mark a promise as broken. */
  async breakPromise(promiseId: string): Promise<SozPromise> {
    return this.client._patch<SozPromise>(
      `/v1/promises/${promiseId}/status`,
      { status: "broken" },
    );
  }

  /** Mark a promise as disputed. */
  async dispute(promiseId: string): Promise<SozPromise> {
    return this.client._patch<SozPromise>(
      `/v1/promises/${promiseId}/status`,
      { status: "disputed" },
    );
  }
}

class EvidenceAPI {
  constructor(private client: SozLedgerClient) {}

  /** Submit evidence for a promise. */
  async submit(
    promiseId: string,
    options: SubmitEvidenceOptions,
  ): Promise<Evidence> {
    return this.client._post<Evidence>(
      `/v1/promises/${promiseId}/evidence`,
      options,
    );
  }

  /** List all evidence for a promise. */
  async list(promiseId: string): Promise<Evidence[]> {
    return this.client._get<Evidence[]>(
      `/v1/promises/${promiseId}/evidence`,
    );
  }
}

class ScoresAPI {
  constructor(private client: SozLedgerClient) {}

  /** Get the current trust score for an entity. */
  async get(entityId: string): Promise<TrustScore> {
    return this.client._get<TrustScore>(`/v1/scores/${entityId}`);
  }

  /** Get historical score snapshots for an entity. */
  async history(entityId: string): Promise<ScoreHistoryResponse> {
    return this.client._get<ScoreHistoryResponse>(
      `/v1/scores/${entityId}/history`,
    );
  }
}

// ── Main client ─────────────────────────────────────────────────────────────

/**
 * Soz Ledger SDK client for the AI Agent Trust Protocol.
 *
 * ```ts
 * const client = new SozLedgerClient("your_api_key");
 * const entity = await client.entities.create({ name: "my-agent", type: "agent" });
 * ```
 */
export class SozLedgerClient {
  private apiKey: string;
  private baseUrl: string;
  private timeout: number;

  /** Sub-API for entity operations. */
  public readonly entities: EntitiesAPI;
  /** Sub-API for promise operations. */
  public readonly promises: PromisesAPI;
  /** Sub-API for evidence operations. */
  public readonly evidence: EvidenceAPI;
  /** Sub-API for trust-score operations. */
  public readonly scores: ScoresAPI;

  constructor(
    apiKey: string,
    baseUrl: string = "http://localhost:8000",
    timeout: number = 30_000,
  ) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.timeout = timeout;

    this.entities = new EntitiesAPI(this);
    this.promises = new PromisesAPI(this);
    this.evidence = new EvidenceAPI(this);
    this.scores = new ScoresAPI(this);
  }

  // ── Internal HTTP helpers ───────────────────────────────────────────────

  private async _request<T>(
    method: string,
    path: string,
    body?: unknown,
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;

    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.apiKey}`,
      "Content-Type": "application/json",
    };

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);

    let response: Response;
    try {
      response = await fetch(url, {
        method,
        headers,
        body: body != null ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });
    } catch (err: unknown) {
      clearTimeout(timer);
      if (err instanceof Error && err.name === "AbortError") {
        throw new SozLedgerError(0, {
          error: "timeout",
          message: `Request timed out after ${this.timeout}ms`,
        });
      }
      throw new SozLedgerError(0, {
        error: "network_error",
        message: err instanceof Error ? err.message : "Unknown network error",
      });
    } finally {
      clearTimeout(timer);
    }

    if (!response.ok) {
      let errorBody: ApiErrorBody | undefined;
      try {
        errorBody = (await response.json()) as ApiErrorBody;
      } catch {
        // response body wasn't valid JSON — leave errorBody undefined
      }
      throw new SozLedgerError(response.status, errorBody);
    }

    return (await response.json()) as T;
  }

  /** @internal */
  async _get<T>(path: string): Promise<T> {
    return this._request<T>("GET", path);
  }

  /** @internal */
  async _post<T>(path: string, body: unknown): Promise<T> {
    return this._request<T>("POST", path, body);
  }

  /** @internal */
  async _patch<T>(path: string, body: unknown): Promise<T> {
    return this._request<T>("PATCH", path, body);
  }
}
