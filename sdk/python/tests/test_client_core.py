from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from soz_ledger.client import SozLedgerClient
from soz_ledger.errors import SozLedgerError
from tests.conftest import ERROR_BODY, make_response


class TestConstructor:
    def test_default_base_url_and_timeout(self):
        with patch("soz_ledger.client.httpx.Client") as MockHttp:
            MockHttp.return_value = MagicMock()
            client = SozLedgerClient("key")

        assert client._base_url == "http://localhost:8000"
        MockHttp.assert_called_once()
        kwargs = MockHttp.call_args
        assert kwargs.kwargs["timeout"] == 30.0

    def test_strips_trailing_slash(self):
        with patch("soz_ledger.client.httpx.Client") as MockHttp:
            MockHttp.return_value = MagicMock()
            client = SozLedgerClient("key", base_url="https://api.example.com///")

        assert client._base_url == "https://api.example.com"

    def test_httpx_client_init_args(self):
        with patch("soz_ledger.client.httpx.Client") as MockHttp:
            MockHttp.return_value = MagicMock()
            SozLedgerClient("my_key", base_url="https://api.test.com", timeout=10.0)

        MockHttp.assert_called_once_with(
            base_url="https://api.test.com",
            headers={"Authorization": "Bearer my_key"},
            timeout=10.0,
        )


class TestRequestDelegation:
    def test_get_delegates_to_request(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, {"id": "1"})

        result = client._get("/v1/test")

        mock_http.request.assert_called_once_with("GET", "/v1/test")
        assert result == {"id": "1"}

    def test_post_delegates_to_request(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, {"id": "1"})

        result = client._post("/v1/test", json={"name": "a"})

        mock_http.request.assert_called_once_with("POST", "/v1/test", json={"name": "a"})
        assert result == {"id": "1"}

    def test_patch_delegates_to_request(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, {"status": "done"})

        result = client._patch("/v1/test", json={"status": "done"})

        mock_http.request.assert_called_once_with("PATCH", "/v1/test", json={"status": "done"})


class TestErrorHandling:
    def test_http_error_raises_soz_ledger_error(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(404, ERROR_BODY)

        with pytest.raises(SozLedgerError) as exc_info:
            client._get("/v1/missing")

        assert exc_info.value.status == 404
        assert exc_info.value.code == "not_found"
        assert exc_info.value.body == ERROR_BODY

    def test_timeout_raises_soz_ledger_error(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.side_effect = httpx.TimeoutException("timed out")

        with pytest.raises(SozLedgerError) as exc_info:
            client._get("/v1/slow")

        assert exc_info.value.status == 0
        assert exc_info.value.code == "timeout"

    def test_network_error_raises_soz_ledger_error(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.side_effect = httpx.ConnectError("connection refused")

        with pytest.raises(SozLedgerError) as exc_info:
            client._get("/v1/down")

        assert exc_info.value.status == 0
        assert exc_info.value.code == "network_error"

    def test_non_json_error_body(self, mock_client):
        client, mock_http = mock_client
        resp = MagicMock()
        resp.status_code = 502
        resp.is_success = False
        resp.json.side_effect = Exception("not json")
        mock_http.request.return_value = resp

        with pytest.raises(SozLedgerError) as exc_info:
            client._get("/v1/bad-gateway")

        assert exc_info.value.status == 502
        assert exc_info.value.body is None


class TestContextManager:
    def test_close_called(self, mock_client):
        client, mock_http = mock_client
        client.close()
        mock_http.close.assert_called_once()

    def test_context_manager(self):
        with patch("soz_ledger.client.httpx.Client") as MockHttp:
            mock_http = MagicMock()
            MockHttp.return_value = mock_http
            with SozLedgerClient("key") as client:
                assert client is not None
            mock_http.close.assert_called_once()
