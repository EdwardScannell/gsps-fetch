"""Replay saved pages: a fetcher with no network, for tests, examples and audits.

A recording is a folder with a `MANIFEST.csv` (columns `url`, `file`, `retrieved_on`,
optional `final_url`) and the saved text files it names. Files must sit inside the
folder. A URL that is not in the recording comes back as gate 404.
"""

from __future__ import annotations

import csv
from pathlib import Path

from gsps.vocab.values import Gate
from pydantic import BaseModel, ConfigDict

from gsps_fetch.protocol import FetchRequest, FetchResult

MANIFEST = "MANIFEST.csv"


class RecordedPage(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: str
    path: Path
    retrieved_on: str
    final_url: str = ""


class RecordedFetcher:
    """Serves pages from a recording folder. Never opens a URL."""

    name = "recorded"

    def __init__(self, folder: Path) -> None:
        self.folder = folder.resolve()
        self.pages: dict[str, RecordedPage] = {}
        with (self.folder / MANIFEST).open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                url = (row.get("url") or "").strip()
                rel = (row.get("file") or "").strip()
                if not url or not rel:
                    raise ValueError(f"{MANIFEST}: every row needs a url and a file")
                path = (self.folder / rel).resolve()
                if not path.is_relative_to(self.folder):
                    raise ValueError(f"{MANIFEST}: {rel!r} is outside the recording")
                if url in self.pages:
                    raise ValueError(f"{MANIFEST}: {url} is recorded twice")
                self.pages[url] = RecordedPage(
                    url=url,
                    path=path,
                    retrieved_on=(row.get("retrieved_on") or "").strip(),
                    final_url=(row.get("final_url") or "").strip(),
                )

    def fetch(self, request: FetchRequest) -> FetchResult:
        page = self.pages.get(request.url.strip())
        if page is None:
            return FetchResult.failure(
                request,
                Gate.NOT_FOUND,
                detail="not in this recording",
                retrieved_on="",
                fetched_by=self.name,
            )
        return FetchResult.success(
            request,
            page.path.read_text(encoding="utf-8"),
            retrieved_on=page.retrieved_on,
            fetched_by=self.name,
            final_url=page.final_url,
        )
