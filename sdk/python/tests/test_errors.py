from __future__ import annotations

import pytest

from soz_ledger.errors import SozLedgerError


class TestSozLedgerError:
    def test_message_from_body(self):
        body = {"error": "not_found", "message": "Entity not found"}
        err = SozLedgerError(404, body)

        assert str(err) == "Entity not found"
        assert err.status == 404
        assert err.code == "not_found"
        assert err.body == body

    def test_detail_body_fastapi_format(self):
        body = {"detail": "Not authenticated"}
        err = SozLedgerError(401, body)

        assert str(err) == "Not authenticated"
        assert err.code is None  # no "error" key

    def test_no_body(self):
        err = SozLedgerError(500)

        assert str(err) == "HTTP 500"
        assert err.code is None
        assert err.body is None

    def test_empty_body(self):
        err = SozLedgerError(502, {})

        assert str(err) == "HTTP 502"
        assert err.code is None
        assert err.body == {}

    def test_isinstance_exception(self):
        err = SozLedgerError(400)
        assert isinstance(err, Exception)
        assert isinstance(err, SozLedgerError)

    def test_code_extraction(self):
        body = {"error": "rate_limited", "message": "Too many requests"}
        err = SozLedgerError(429, body)
        assert err.code == "rate_limited"
