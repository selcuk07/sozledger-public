import type {
  CreateEntityOptions,
  CreatePromiseOptions,
  Entity,
  Evidence,
  Promise as SozPromise,
  ScoreHistoryResponse,
  SubmitEvidenceOptions,
  TrustScore,
} from "./types";

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
 * const entity = await client.entities.create({ name: "my-agent", type: "ai_agent" });
 * ```
 *
 * **Note:** This is a stub -- method bodies will be implemented in a future
 * release.  All methods currently throw a "Not implemented yet" error.
 */
export class SozLedgerClient {
  private apiKey: string;
  private baseUrl: string;

  /** Sub-API for entity operations. */
  public readonly entities: EntitiesAPI;
  /** Sub-API for promise operations. */
  public readonly promises: PromisesAPI;
  /** Sub-API for evidence operations. */
  public readonly evidence: EvidenceAPI;
  /** Sub-API for trust-score operations. */
  public readonly scores: ScoresAPI;

  constructor(apiKey: string, baseUrl: string = "http://localhost:8000") {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/+$/, "");

    this.entities = new EntitiesAPI(this);
    this.promises = new PromisesAPI(this);
    this.evidence = new EvidenceAPI(this);
    this.scores = new ScoresAPI(this);
  }

  // ── Internal HTTP helpers (stubs) ───────────────────────────────────────

  /** @internal */
  async _get<T>(path: string): Promise<T> {
    throw new Error(
      `Not implemented yet: GET ${this.baseUrl}${path}`,
    );
  }

  /** @internal */
  async _post<T>(path: string, body: Record<string, unknown>): Promise<T> {
    throw new Error(
      `Not implemented yet: POST ${this.baseUrl}${path}`,
    );
  }

  /** @internal */
  async _patch<T>(path: string, body: Record<string, unknown>): Promise<T> {
    throw new Error(
      `Not implemented yet: PATCH ${this.baseUrl}${path}`,
    );
  }
}
