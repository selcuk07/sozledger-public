from __future__ import annotations

from typing import Any


class SozLedgerError(Exception):
    """Error raised by the Soz Ledger SDK for HTTP and network failures.

    Attributes:
        status: HTTP status code (``0`` for network / timeout errors).
        code:   Machine-readable error string from the API, if available.
        body:   Full parsed error response dict, when available.
    """

    def __init__(self, status: int, body: dict[str, Any] | None = None) -> None:
        # Handle both FastAPI {"detail": "..."} and {"error": "...", "message": "..."} formats
        if body:
            msg = body.get("message") or body.get("detail") or f"HTTP {status}"
        else:
            msg = f"HTTP {status}"

        super().__init__(msg)
        self.status = status
        self.code: str | None = body.get("error") if body else None
        self.body = body
