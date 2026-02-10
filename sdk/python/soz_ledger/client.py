from __future__ import annotations

import httpx

from soz_ledger.errors import SozLedgerError
from soz_ledger.models import (
    DeliveryLog,
    Entity,
    Evidence,
    Promise,
    ScoreHistoryEntry,
    ScoreHistoryResponse,
    TrustScore,
    Webhook,
    WebhookWithSecret,
    _from_dict,
)


class _EntitiesAPI:
    def __init__(self, client: SozLedgerClient) -> None:
        self._client = client

    def create(
        self,
        name: str,
        type: str,
        public_key: str | None = None,
        metadata: dict | None = None,
    ) -> Entity:
        data: dict = {"name": name, "type": type}
        if public_key is not None:
            data["public_key"] = public_key
        if metadata is not None:
            data["metadata"] = metadata

        resp = self._client._post("/v1/entities", json=data)
        return _from_dict(Entity, resp)

    def get(self, entity_id: str) -> Entity:
        resp = self._client._get(f"/v1/entities/{entity_id}")
        return _from_dict(Entity, resp)

    def score(self, entity_id: str) -> TrustScore:
        resp = self._client._get(f"/v1/entities/{entity_id}/score")
        return _from_dict(TrustScore, resp)


class _PromisesAPI:
    def __init__(self, client: SozLedgerClient) -> None:
        self._client = client

    def create(
        self,
        promisor_id: str,
        promisee_id: str,
        description: str,
        deadline: str | None = None,
        category: str = "custom",
    ) -> Promise:
        data: dict = {
            "promisor_id": promisor_id,
            "promisee_id": promisee_id,
            "description": description,
            "category": category,
        }
        if deadline is not None:
            data["deadline"] = deadline

        resp = self._client._post("/v1/promises", json=data)
        return _from_dict(Promise, resp)

    def get(self, promise_id: str) -> Promise:
        resp = self._client._get(f"/v1/promises/{promise_id}")
        return _from_dict(Promise, resp)

    def fulfill(self, promise_id: str) -> Promise:
        resp = self._client._patch(
            f"/v1/promises/{promise_id}/status", json={"status": "fulfilled"}
        )
        return _from_dict(Promise, resp)

    def break_promise(self, promise_id: str) -> Promise:
        resp = self._client._patch(
            f"/v1/promises/{promise_id}/status", json={"status": "broken"}
        )
        return _from_dict(Promise, resp)

    def dispute(self, promise_id: str) -> Promise:
        resp = self._client._patch(
            f"/v1/promises/{promise_id}/status", json={"status": "disputed"}
        )
        return _from_dict(Promise, resp)


class _EvidenceAPI:
    def __init__(self, client: SozLedgerClient) -> None:
        self._client = client

    def submit(
        self,
        promise_id: str,
        type: str,
        submitted_by: str,
        payload: dict | None = None,
    ) -> Evidence:
        data: dict = {"type": type, "submitted_by": submitted_by}
        if payload is not None:
            data["payload"] = payload

        resp = self._client._post(
            f"/v1/promises/{promise_id}/evidence", json=data
        )
        return _from_dict(Evidence, resp)

    def list(self, promise_id: str) -> list[Evidence]:
        resp = self._client._get(f"/v1/promises/{promise_id}/evidence")
        return [_from_dict(Evidence, e) for e in resp]


class _ScoresAPI:
    def __init__(self, client: SozLedgerClient) -> None:
        self._client = client

    def get(self, entity_id: str) -> TrustScore:
        resp = self._client._get(f"/v1/scores/{entity_id}")
        return _from_dict(TrustScore, resp)

    def history(self, entity_id: str) -> ScoreHistoryResponse:
        resp = self._client._get(f"/v1/scores/{entity_id}/history")
        entries = [
            _from_dict(ScoreHistoryEntry, h) for h in resp.get("history", [])
        ]
        return ScoreHistoryResponse(entity_id=resp["entity_id"], history=entries)


class _WebhooksAPI:
    def __init__(self, client: SozLedgerClient) -> None:
        self._client = client

    def create(
        self,
        url: str,
        event_types: list[str],
    ) -> WebhookWithSecret:
        data: dict = {"url": url, "event_types": event_types}
        resp = self._client._post("/v1/webhooks", json=data)
        return _from_dict(WebhookWithSecret, resp)

    def list(self) -> list[Webhook]:
        resp = self._client._get("/v1/webhooks")
        return [_from_dict(Webhook, w) for w in resp]

    def get(self, webhook_id: str) -> Webhook:
        resp = self._client._get(f"/v1/webhooks/{webhook_id}")
        return _from_dict(Webhook, resp)

    def update(
        self,
        webhook_id: str,
        url: str | None = None,
        event_types: list[str] | None = None,
        is_active: bool | None = None,
    ) -> Webhook:
        data: dict = {}
        if url is not None:
            data["url"] = url
        if event_types is not None:
            data["event_types"] = event_types
        if is_active is not None:
            data["is_active"] = is_active
        resp = self._client._patch(f"/v1/webhooks/{webhook_id}", json=data)
        return _from_dict(Webhook, resp)

    def delete(self, webhook_id: str) -> None:
        self._client._delete(f"/v1/webhooks/{webhook_id}")

    def logs(self, webhook_id: str) -> list[DeliveryLog]:
        resp = self._client._get(f"/v1/webhooks/{webhook_id}/logs")
        return [_from_dict(DeliveryLog, log) for log in resp]


class SozLedgerClient:
    """Soz Ledger SDK client for the AI Agent Trust Protocol.

    Usage::

        client = SozLedgerClient("your_api_key")
        agent = client.entities.create(name="my-agent", type="agent")

    The client can also be used as a context manager::

        with SozLedgerClient("your_api_key") as client:
            agent = client.entities.create(name="my-agent", type="agent")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:8000",
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._http = httpx.Client(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

        self.entities = _EntitiesAPI(self)
        self.promises = _PromisesAPI(self)
        self.evidence = _EvidenceAPI(self)
        self.scores = _ScoresAPI(self)
        self.webhooks = _WebhooksAPI(self)

    # ── Internal HTTP helpers ────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> dict | list:
        try:
            resp = self._http.request(method, path, **kwargs)
        except httpx.TimeoutException as exc:
            raise SozLedgerError(0, {"error": "timeout", "message": str(exc)}) from exc
        except httpx.HTTPError as exc:
            raise SozLedgerError(0, {"error": "network_error", "message": str(exc)}) from exc

        if not resp.is_success:
            body: dict | None = None
            try:
                body = resp.json()
            except Exception:
                pass
            raise SozLedgerError(resp.status_code, body)

        return resp.json()

    def _get(self, path: str) -> dict | list:
        return self._request("GET", path)

    def _post(self, path: str, json: dict) -> dict:
        return self._request("POST", path, json=json)

    def _patch(self, path: str, json: dict) -> dict:
        return self._request("PATCH", path, json=json)

    def _delete(self, path: str) -> None:
        try:
            resp = self._http.request("DELETE", path)
        except httpx.TimeoutException as exc:
            raise SozLedgerError(0, {"error": "timeout", "message": str(exc)}) from exc
        except httpx.HTTPError as exc:
            raise SozLedgerError(0, {"error": "network_error", "message": str(exc)}) from exc

        if not resp.is_success:
            body: dict | None = None
            try:
                body = resp.json()
            except Exception:
                pass
            raise SozLedgerError(resp.status_code, body)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> SozLedgerClient:
        return self

    def __exit__(self, *args) -> None:
        self.close()
