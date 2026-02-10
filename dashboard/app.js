// Soz Ledger Dashboard

(function () {
  "use strict";

  // ---- State ----
  const state = {
    baseUrl: "",
    apiKey: "",
    entityId: "",
    entity: null,
    score: null,
    history: null,
    promises: [],
  };

  let historyChart = null;

  // ---- DOM refs ----
  const $ = (sel) => document.querySelector(sel);
  const loginView = $("#login-view");
  const dashboardView = $("#dashboard-view");
  const loginForm = $("#login-form");
  const loginError = $("#login-error");
  const loadingOverlay = $("#loading-overlay");

  // ---- API module ----
  const api = {
    async request(path) {
      const url = `${state.baseUrl}${path}`;
      const headers = { Accept: "application/json" };
      if (state.apiKey) {
        headers["Authorization"] = `Bearer ${state.apiKey}`;
      }
      const res = await fetch(url, { headers });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        const msg = (body && body.detail) || (body && body.message) || res.statusText;
        throw new Error(`${res.status}: ${msg}`);
      }
      return res.json();
    },

    getEntity(entityId) {
      return this.request(`/v1/entities/${entityId}`);
    },

    getScore(entityId) {
      return this.request(`/v1/scores/${entityId}`);
    },

    getScoreHistory(entityId) {
      return this.request(`/v1/scores/${entityId}/history`);
    },

    getPromises(entityId, status) {
      let path = `/v1/entities/${entityId}/promises?limit=200`;
      if (status) path += `&status=${status}`;
      return this.request(path);
    },

    getPromise(promiseId) {
      return this.request(`/v1/promises/${promiseId}`);
    },

    getEvidence(promiseId) {
      return this.request(`/v1/promises/${promiseId}/evidence`);
    },
  };

  // ---- Level helpers ----
  function levelClass(level) {
    if (!level) return "level-unrated";
    const l = level.toLowerCase();
    if (l.includes("exceptional")) return "level-exceptional";
    if (l.includes("high")) return "level-high";
    if (l.includes("reliable")) return "level-reliable";
    if (l.includes("developing")) return "level-developing";
    if (l.includes("low")) return "level-low";
    return "level-unrated";
  }

  function levelColor(level) {
    const cls = levelClass(level);
    const map = {
      "level-exceptional": "#f59e0b",
      "level-high": "#3b82f6",
      "level-reliable": "#22c55e",
      "level-developing": "#eab308",
      "level-low": "#ef4444",
      "level-unrated": "#9ca3af",
    };
    return map[cls] || "#9ca3af";
  }

  // ---- Render functions ----

  function renderScoreCard(score) {
    const ring = $("#score-ring-fill");
    const value = $("#score-value");
    const badge = $("#level-badge");
    const subtitle = $("#score-subtitle");

    if (!score || score.overall_score == null) {
      ring.style.strokeDashoffset = "326.7";
      ring.style.stroke = "#9ca3af";
      value.textContent = "--";
      badge.textContent = score ? score.level || "Unrated" : "Unrated";
      badge.className = "level-badge level-unrated";
      subtitle.textContent = "Not enough promises to rate";
      return;
    }

    const pct = score.overall_score;
    const offset = 326.7 * (1 - pct);
    const color = levelColor(score.level);

    ring.style.strokeDashoffset = offset.toString();
    ring.style.stroke = color;
    value.textContent = (pct * 100).toFixed(0);
    badge.textContent = score.level;
    badge.className = `level-badge ${levelClass(score.level)}`;
    subtitle.textContent = `Score: ${pct.toFixed(3)} | Version ${score.score_version || "?"}`;
  }

  function renderStats(score) {
    $("#stat-total").textContent = score ? score.total_promises : 0;
    $("#stat-fulfilled").textContent = score ? score.fulfilled_count : 0;
    $("#stat-broken").textContent = score ? score.broken_count : 0;
    $("#stat-streak").textContent = score ? score.streak : 0;
  }

  function renderHistoryChart(history) {
    const canvas = $("#history-chart");
    const empty = $("#history-empty");

    if (!history || !history.history || history.history.length === 0) {
      canvas.parentElement.style.display = "none";
      empty.hidden = false;
      return;
    }

    canvas.parentElement.style.display = "block";
    empty.hidden = true;

    // Data is newest-first, reverse for chronological
    const entries = [...history.history].reverse();
    const labels = entries.map((e) => {
      if (!e.timestamp) return "?";
      const d = new Date(e.timestamp);
      return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
    });
    const scores = entries.map((e) => e.score);

    if (historyChart) {
      historyChart.destroy();
    }

    historyChart = new Chart(canvas, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Trust Score",
            data: scores,
            borderColor: "#4f46e5",
            backgroundColor: "rgba(79, 70, 229, 0.1)",
            fill: true,
            tension: 0.3,
            pointBackgroundColor: "#4f46e5",
            pointRadius: 4,
            pointHoverRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `Score: ${ctx.parsed.y != null ? ctx.parsed.y.toFixed(3) : "--"}`,
            },
          },
        },
        scales: {
          y: {
            min: 0,
            max: 1,
            ticks: { stepSize: 0.2 },
            grid: { color: "#f3f4f6" },
          },
          x: {
            grid: { display: false },
          },
        },
      },
    });
  }

  function renderCategoryScores(score) {
    const container = $("#category-scores");
    const empty = $("#category-empty");

    const cats = score && score.category_scores ? score.category_scores : null;

    if (!cats || Object.keys(cats).length === 0) {
      container.innerHTML = "";
      empty.hidden = false;
      return;
    }

    empty.hidden = true;

    container.innerHTML = Object.entries(cats)
      .map(([cat, val]) => {
        const pct = ((val || 0) * 100).toFixed(0);
        return `
        <div class="category-bar-row">
          <span class="category-bar-label">${cat}</span>
          <div class="category-bar-track">
            <div class="category-bar-fill" style="width:${pct}%;background:${levelColor(score.level)}"></div>
          </div>
          <span class="category-bar-value">${pct}%</span>
        </div>`;
      })
      .join("");
  }

  function formatDate(iso) {
    if (!iso) return "--";
    const d = new Date(iso);
    return d.toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  function renderPromisesTable(promises) {
    const tbody = $("#promises-tbody");
    const empty = $("#promises-empty");

    if (!promises || promises.length === 0) {
      tbody.innerHTML = "";
      empty.hidden = false;
      return;
    }

    empty.hidden = true;

    tbody.innerHTML = promises
      .map((p) => {
        const counterparty =
          p.promisor_id === state.entityId ? p.promisee_id : p.promisor_id;
        const shortId = counterparty.substring(0, 8) + "...";
        return `
        <tr data-promise-id="${p.id}">
          <td><span class="status-badge status-${p.status}">${p.status}</span></td>
          <td class="truncate" title="${escapeHtml(p.description)}">${escapeHtml(p.description)}</td>
          <td><span class="category-tag">${p.category}</span></td>
          <td title="${counterparty}">${shortId}</td>
          <td>${formatDate(p.created_at)}</td>
          <td>${formatDate(p.deadline)}</td>
        </tr>`;
      })
      .join("");

    // Attach click handlers
    tbody.querySelectorAll("tr[data-promise-id]").forEach((row) => {
      row.addEventListener("click", () => {
        openPromiseDetail(row.dataset.promiseId);
      });
    });
  }

  async function openPromiseDetail(promiseId) {
    const panel = $("#promise-detail");
    const body = $("#detail-body");

    panel.hidden = false;
    body.innerHTML = '<div class="spinner" style="margin:32px auto"></div>';

    try {
      const [promise, evidenceRes] = await Promise.all([
        api.getPromise(promiseId),
        api.getEvidence(promiseId),
      ]);

      const evidenceList =
        evidenceRes && evidenceRes.evidence ? evidenceRes.evidence : evidenceRes || [];
      const items = Array.isArray(evidenceList) ? evidenceList : [];

      body.innerHTML = `
        <div class="detail-field">
          <div class="detail-field-label">Status</div>
          <div class="detail-field-value"><span class="status-badge status-${promise.status}">${promise.status}</span></div>
        </div>
        <div class="detail-field">
          <div class="detail-field-label">Description</div>
          <div class="detail-field-value">${escapeHtml(promise.description)}</div>
        </div>
        <div class="detail-field">
          <div class="detail-field-label">Category</div>
          <div class="detail-field-value"><span class="category-tag">${promise.category}</span></div>
        </div>
        <div class="detail-field">
          <div class="detail-field-label">Promisor</div>
          <div class="detail-field-value" style="font-size:0.8rem;word-break:break-all">${promise.promisor_id}</div>
        </div>
        <div class="detail-field">
          <div class="detail-field-label">Promisee</div>
          <div class="detail-field-value" style="font-size:0.8rem;word-break:break-all">${promise.promisee_id}</div>
        </div>
        <div class="detail-field">
          <div class="detail-field-label">Created</div>
          <div class="detail-field-value">${formatDate(promise.created_at)}</div>
        </div>
        <div class="detail-field">
          <div class="detail-field-label">Deadline</div>
          <div class="detail-field-value">${formatDate(promise.deadline)}</div>
        </div>
        ${promise.fulfilled_at ? `
        <div class="detail-field">
          <div class="detail-field-label">Fulfilled At</div>
          <div class="detail-field-value">${formatDate(promise.fulfilled_at)}</div>
        </div>` : ""}
        <div class="detail-field">
          <div class="detail-field-label">Evidence (${items.length})</div>
          <div class="detail-field-value">
            ${items.length === 0 ? '<p class="evidence-empty">No evidence submitted.</p>' : `
              <ul class="evidence-list">
                ${items.map((e) => `
                  <li class="evidence-item">
                    <div class="evidence-type">${escapeHtml(e.evidence_type || e.type || "unknown")}</div>
                    <div class="evidence-content">${escapeHtml(e.content || "")}</div>
                    <div class="evidence-meta">By ${(e.submitted_by || "").substring(0, 8)}... on ${formatDate(e.created_at)}</div>
                  </li>
                `).join("")}
              </ul>
            `}
          </div>
        </div>
      `;
    } catch (err) {
      body.innerHTML = `<div class="error-message">${escapeHtml(err.message)}</div>`;
    }
  }

  function escapeHtml(str) {
    if (!str) return "";
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // ---- Main flow ----

  async function loadDashboard() {
    loadingOverlay.hidden = false;

    try {
      const [entity, score, history, promises] = await Promise.all([
        api.getEntity(state.entityId),
        api.getScore(state.entityId),
        api.getScoreHistory(state.entityId),
        api.getPromises(state.entityId),
      ]);

      state.entity = entity;
      state.score = score;
      state.history = history;
      state.promises = promises;

      $("#header-entity-name").textContent = entity.name || state.entityId;
      renderScoreCard(score);
      renderStats(score);
      renderHistoryChart(history);
      renderCategoryScores(score);
      renderPromisesTable(promises);
    } catch (err) {
      alert("Failed to load dashboard: " + err.message);
    } finally {
      loadingOverlay.hidden = true;
    }
  }

  function showDashboard() {
    loginView.hidden = true;
    dashboardView.hidden = false;
  }

  function showLogin() {
    loginView.hidden = false;
    dashboardView.hidden = true;
    loginView.style.display = "flex";
  }

  function logout() {
    sessionStorage.removeItem("soz_baseUrl");
    sessionStorage.removeItem("soz_apiKey");
    sessionStorage.removeItem("soz_entityId");
    state.baseUrl = "";
    state.apiKey = "";
    state.entityId = "";
    state.entity = null;
    state.score = null;
    state.history = null;
    state.promises = [];
    if (historyChart) {
      historyChart.destroy();
      historyChart = null;
    }
    showLogin();
  }

  // ---- Event handlers ----

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    loginError.hidden = true;

    const baseUrl = $("#base-url").value.replace(/\/+$/, "");
    const apiKey = $("#api-key").value.trim();
    const entityId = $("#entity-id").value.trim();

    if (!apiKey || !entityId) {
      loginError.textContent = "API Key and Entity ID are required.";
      loginError.hidden = false;
      return;
    }

    state.baseUrl = baseUrl;
    state.apiKey = apiKey;
    state.entityId = entityId;

    // Test connection
    try {
      await api.getEntity(entityId);
    } catch (err) {
      loginError.textContent = "Connection failed: " + err.message;
      loginError.hidden = false;
      return;
    }

    sessionStorage.setItem("soz_baseUrl", baseUrl);
    sessionStorage.setItem("soz_apiKey", apiKey);
    sessionStorage.setItem("soz_entityId", entityId);

    showDashboard();
    loadDashboard();
  });

  $("#refresh-btn").addEventListener("click", () => {
    loadDashboard();
  });

  $("#logout-btn").addEventListener("click", logout);

  $("#detail-close").addEventListener("click", () => {
    $("#promise-detail").hidden = true;
  });

  // Close detail panel on backdrop click
  $("#promise-detail").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) {
      e.currentTarget.hidden = true;
    }
  });

  // Status filter
  $("#promise-status-filter").addEventListener("change", async (e) => {
    const status = e.target.value;
    try {
      const promises = await api.getPromises(state.entityId, status);
      state.promises = promises;
      renderPromisesTable(promises);
    } catch (err) {
      console.error("Failed to filter promises:", err);
    }
  });

  // ---- Session restore ----
  const saved = {
    baseUrl: sessionStorage.getItem("soz_baseUrl"),
    apiKey: sessionStorage.getItem("soz_apiKey"),
    entityId: sessionStorage.getItem("soz_entityId"),
  };

  if (saved.baseUrl && saved.apiKey && saved.entityId) {
    state.baseUrl = saved.baseUrl;
    state.apiKey = saved.apiKey;
    state.entityId = saved.entityId;
    showDashboard();
    loadDashboard();
  } else {
    showLogin();
  }
})();
