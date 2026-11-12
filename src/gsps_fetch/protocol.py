"""The fetcher contract: a request goes in, a result with receipts comes out.

Doctrine kept here:

* The engine makes no network calls. Anything that opens a page implements `Fetcher`
  and lives outside the core.
* A result always names its gate. A failure is a result too, never an exception, so it
  can be logged and turned into a follow-up item.
* The text is hashed after normalizing line endings, so the same page gives the same
  hash on every platform.
"""

from __future__ import annotations

import hashlib
from typing import Protocol, runtime_checkable

from gsps.vocab.values import Gate
from pydantic import BaseModel, ConfigDict


def normalize_newlines(text: str) -> str:
    """CRLF and lone CR become LF."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def content_hash(text: str) -> str:
    """SHA-256 of the UTF-8 text with line endings normalized."""
    return hashlib.sha256(normalize_newlines(text).encode("utf-8")).hexdigest()


class FetchRequest(BaseModel):
    """What to open, how it was cleared, and who asked."""

    model_config = ConfigDict(frozen=True)

    url: str
    gate: Gate
    requested_by: str = "keeper"
    anchor_id: str = ""
    parent_url: str = ""  # required for a chained gate (enforced by the guard, phase 3)


class FetchResult(BaseModel):
    """What came back. `text` is None when nothing was returned."""

    model_config = ConfigDict(frozen=True)

    url: str
    final_url: str
    gate: Gate
    text: str | None = None
    sha256: str = ""
    retrieved_on: str
    fetched_by: str
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.gate.cleared and self.text is not None

    @classmethod
    def success(
        cls,
        request: FetchRequest,
        text: str,
        *,
        retrieved_on: str,
        fetched_by: str,
        final_url: str = "",
    ) -> FetchResult:
        return cls(
            url=request.url,
            final_url=final_url or request.url,
            gate=request.gate,
            text=text,
            sha256=content_hash(text),
            retrieved_on=retrieved_on,
            fetched_by=fetched_by,
        )

    @classmethod
    def failure(
        cls,
        request: FetchRequest,
        gate: Gate,
        *,
        detail: str,
        retrieved_on: str,
        fetched_by: str,
    ) -> FetchResult:
        if gate.cleared:
            raise ValueError(f"a failure needs a failing gate, not {gate.value!r}")
        return cls(
            url=request.url,
            final_url=request.url,
            gate=gate,
            retrieved_on=retrieved_on,
            fetched_by=fetched_by,
            detail=detail,
        )


@runtime_checkable
class Fetcher(Protocol):
    """Anything that can open a page. Implementations live outside the core engine."""

    name: str

    def fetch(self, request: FetchRequest) -> FetchResult: ...
