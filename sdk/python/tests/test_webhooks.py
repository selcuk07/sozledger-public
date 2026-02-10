from __future__ import annotations

from soz_ledger.models import DeliveryLog, Webhook, WebhookWithSecret
from tests.conftest import (
    DELIVERY_LOG_DATA,
    WEBHOOK_DATA,
    WEBHOOK_WITH_SECRET_DATA,
    make_response,
)


class TestWebhooksCreate:
    def test_sends_post(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(201, WEBHOOK_WITH_SECRET_DATA)

        wh = client.webhooks.create(
            url="https://example.com/webhook",
            event_types=["promise.created", "promise.fulfilled"],
        )

        mock_http.request.assert_called_once_with(
            "POST",
            "/v1/webhooks",
            json={
                "url": "https://example.com/webhook",
                "event_types": ["promise.created", "promise.fulfilled"],
            },
        )
        assert isinstance(wh, WebhookWithSecret)
        assert wh.secret == "whsec_test_secret_123"


class TestWebhooksList:
    def test_returns_list(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, [WEBHOOK_DATA])

        webhooks = client.webhooks.list()

        mock_http.request.assert_called_once_with("GET", "/v1/webhooks")
        assert len(webhooks) == 1
        assert isinstance(webhooks[0], Webhook)
        assert webhooks[0].id == "wh_abc123"


class TestWebhooksGet:
    def test_returns_webhook(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, WEBHOOK_DATA)

        wh = client.webhooks.get("wh_abc123")

        mock_http.request.assert_called_once_with("GET", "/v1/webhooks/wh_abc123")
        assert isinstance(wh, Webhook)
        assert wh.url == "https://example.com/webhook"


class TestWebhooksUpdate:
    def test_sends_patch(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, WEBHOOK_DATA)

        wh = client.webhooks.update("wh_abc123", is_active=False)

        mock_http.request.assert_called_once_with(
            "PATCH", "/v1/webhooks/wh_abc123", json={"is_active": False}
        )
        assert isinstance(wh, Webhook)


class TestWebhooksDelete:
    def test_sends_delete(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(204, None)

        result = client.webhooks.delete("wh_abc123")

        mock_http.request.assert_called_once_with("DELETE", "/v1/webhooks/wh_abc123")
        assert result is None


class TestWebhooksLogs:
    def test_returns_logs(self, mock_client):
        client, mock_http = mock_client
        mock_http.request.return_value = make_response(200, [DELIVERY_LOG_DATA])

        logs = client.webhooks.logs("wh_abc123")

        mock_http.request.assert_called_once_with("GET", "/v1/webhooks/wh_abc123/logs")
        assert len(logs) == 1
        assert isinstance(logs[0], DeliveryLog)
        assert logs[0].success is True
