import httpx
from soz_ledger.models import Entity, Evidence, Promise, TrustScore


class _EntitiesAPI:
    def __init__(self, client: "SozLedgerClient"):
        self._client = client

    def create(self, name: str, type: str, public_key: str | None = None, metadata: dict | None = None) -> Entity:
        data = {"name": name, "type": type}
        if public_key:
            data["public_key"] = public_key
        if metadata:
            data["metadata"] = metadata

        resp = self._client._post("/v1/entities", json=data)
        return Entity(**resp)

    def get(self, entity_id: str) -> Entity:
        resp = self._client._get(f"/v1/entities/{entity_id}")
        return Entity(**resp)

    def score(self, entity_id: str) -> dict:
        return self._client._get(f"/v1/entities/{entity_id}/score")


class _PromisesAPI:
    def __init__(self, client: "SozLedgerClient"):
        self._client = client

    def create(
        self,
        promisor_id: str,
        promisee_id: str,
        description: str,
        deadline: str | None = None,
        category: str = "custom",
    ) -> Promise:
        data = {
            "promisor_id": promisor_id,
            "promisee_id": promisee_id,
            "description": description,
            "category": category,
        }
        if deadline:
            data["deadline"] = deadline

        resp = self._client._post("/v1/promises", json=data)
        return Promise(**resp)

    def get(self, promise_id: str) -> Promise:
        resp = self._client._get(f"/v1/promises/{promise_id}")
        return Promise(**resp)

    def fulfill(self, promise_id: str) -> Promise:
        resp = self._client._patch(f"/v1/promises/{promise_id}/status", json={"status": "fulfilled"})
        return Promise(**resp)

    def break_promise(self, promise_id: str) -> Promise:
        resp = self._client._patch(f"/v1/promises/{promise_id}/status", json={"status": "broken"})
        return Promise(**resp)

    def dispute(self, promise_id: str) -> Promise:
        resp = self._client._patch(f"/v1/promises/{promise_id}/status", json={"status": "disputed"})
        return Promise(**resp)


class _EvidenceAPI:
    def __init__(self, client: "SozLedgerClient"):
        self._client = client

    def submit(
        self,
        promise_id: str,
        type: str,
        submitted_by: str,
        payload: dict | None = None,
    ) -> Evidence:
        data = {"type": type, "submitted_by": submitted_by}
        if payload:
            data["payload"] = payload

        resp = self._client._post(f"/v1/promises/{promise_id}/evidence", json=data)
        return Evidence(**resp)

    def list(self, promise_id: str) -> list[Evidence]:
        resp = self._client._get(f"/v1/promises/{promise_id}/evidence")
        return [Evidence(**e) for e in resp]


class _ScoresAPI:
    def __init__(self, client: "SozLedgerClient"):
        self._client = client

    def get(self, entity_id: str) -> TrustScore:
        resp = self._client._get(f"/v1/scores/{entity_id}")
        return TrustScore(**resp)

    def history(self, entity_id: str) -> dict:
        return self._client._get(f"/v1/scores/{entity_id}/history")


class SozLedgerClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._http = httpx.Client(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0,
        )

        self.entities = _EntitiesAPI(self)
        self.promises = _PromisesAPI(self)
        self.evidence = _EvidenceAPI(self)
        self.scores = _ScoresAPI(self)

    def _get(self, path: str) -> dict | list:
        resp = self._http.get(path)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, json: dict) -> dict:
        resp = self._http.post(path, json=json)
        resp.raise_for_status()
        return resp.json()

    def _patch(self, path: str, json: dict) -> dict:
        resp = self._http.patch(path, json=json)
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
