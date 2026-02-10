/**
 * Soz Ledger -- JavaScript Quick Start (raw HTTP / fetch)
 * ========================================================
 * No SDK required.  Uses the built-in fetch() API available in
 * Node 18+ and all modern browsers.
 *
 * Run:
 *   node quickstart.js
 */

const BASE_URL = "http://localhost:8000";
const API_KEY = "your_api_key";

/** Helper: make an authenticated request to the Soz Ledger API. */
async function api(method, path, body) {
  const options = {
    method,
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
  };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${method} ${path} failed (${res.status}): ${text}`);
  }
  return res.json();
}

async function main() {
  // ── 1. Register two entities ──────────────────────────────────────────────
  //    Every participant -- agent, service, human -- is an entity.
  const agentA = await api("POST", "/v1/entities", {
    name: "summary-agent",
    type: "ai_agent",
  });
  console.log("Created entity:", agentA.id);

  const agentB = await api("POST", "/v1/entities", {
    name: "review-service",
    type: "service",
  });
  console.log("Created entity:", agentB.id);

  // ── 2. Create a promise ───────────────────────────────────────────────────
  //    Agent A promises Agent B that it will deliver a summary.
  const promise = await api("POST", "/v1/promises", {
    promisor_id: agentA.id,
    promisee_id: agentB.id,
    description: "Summarise the quarterly report into three bullet points",
    category: "task_completion",
    deadline: "2025-12-31T23:59:59Z",
  });
  console.log("Promise created:", promise.id, "status:", promise.status);

  // ── 3. Submit evidence ────────────────────────────────────────────────────
  //    Attach the output artefact so it can be verified later.
  const evidence = await api(
    "POST",
    `/v1/promises/${promise.id}/evidence`,
    {
      type: "output",
      submitted_by: agentA.id,
      payload: {
        bullets: [
          "Revenue grew 12% year-over-year.",
          "Customer churn decreased by 3 percentage points.",
          "New enterprise contracts doubled compared to Q2.",
        ],
      },
    }
  );
  console.log("Evidence submitted:", evidence.id);

  // ── 4. Fulfill the promise ────────────────────────────────────────────────
  const fulfilled = await api(
    "PATCH",
    `/v1/promises/${promise.id}/status`,
    { status: "fulfilled" }
  );
  console.log("Promise status:", fulfilled.status);

  // ── 5. Check the trust score ──────────────────────────────────────────────
  const score = await api("GET", `/v1/scores/${agentA.id}`);
  console.log("Trust score for", agentA.name + ":");
  console.log("  overall :", score.overall_score);
  console.log("  level   :", score.level);
  console.log("  fulfilled / total :", score.fulfilled_count, "/", score.total_promises);

  console.log("\nDone.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
