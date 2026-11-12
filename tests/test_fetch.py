"""Phase 1: the fetcher contract and the replay fetcher."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from gsps.vocab.values import Gate
from pydantic import ValidationError

from gsps_fetch import Fetcher, FetchRequest, FetchResult, RecordedFetcher, content_hash
from tests.conftest import FIXTURES, ROOT

RECORDING = FIXTURES / "recorded"
URL = "https://stats.example.gov/release/payrolls-2026-10"


def request(url: str = URL, gate: Gate = Gate.PASTE) -> FetchRequest:
    return FetchRequest(url=url, gate=gate, anchor_id="LAB-013")


def test_recorded_url_returns_text_with_receipts() -> None:
    result = RecordedFetcher(RECORDING).fetch(request())
    assert result.ok
    assert result.gate is Gate.PASTE
    assert result.text is not None and "120,000" in result.text
    assert result.sha256 == content_hash(result.text)
    assert result.retrieved_on == "2026-11-07"
    assert result.fetched_by == "recorded"
    assert result.final_url == URL


def test_recorded_short_url_reports_its_final_url() -> None:
    result = RecordedFetcher(RECORDING).fetch(request("https://stats.example.gov/r/oct"))
    assert result.final_url == URL


def test_unknown_url_is_a_404_result_not_an_exception() -> None:
    result = RecordedFetcher(RECORDING).fetch(request("https://stats.example.gov/missing"))
    assert not result.ok
    assert result.gate is Gate.NOT_FOUND
    assert result.text is None and result.sha256 == ""


def test_hash_ignores_line_endings() -> None:
    assert content_hash("a\r\nb\rc\n") == content_hash("a\nb\nc\n")


def test_hash_changes_with_one_character() -> None:
    assert content_hash("rose by 120,000") == content_hash("rose by 120,000")
    assert content_hash("rose by 120,000") != content_hash("rose by 120,001")


def test_results_are_frozen() -> None:
    result = RecordedFetcher(RECORDING).fetch(request())
    with pytest.raises(ValidationError):
        result.text = "edited"  # type: ignore[misc]


def test_failure_needs_a_failing_gate() -> None:
    with pytest.raises(ValueError, match="failing gate"):
        FetchResult.failure(request(), Gate.PASTE, detail="x", retrieved_on="", fetched_by="t")


def test_recorded_fetcher_satisfies_the_protocol() -> None:
    assert isinstance(RecordedFetcher(RECORDING), Fetcher)


def test_recording_cannot_point_outside_its_folder(tmp_path: Path) -> None:
    (tmp_path / "MANIFEST.csv").write_text(
        "url,file,retrieved_on\nhttps://x.example/,../secret.txt,2026-11-07\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="outside the recording"):
        RecordedFetcher(tmp_path)


def test_recording_rejects_duplicate_and_incomplete_rows(tmp_path: Path) -> None:
    (tmp_path / "p.txt").write_text("x", encoding="utf-8")
    manifest = tmp_path / "MANIFEST.csv"
    manifest.write_text(
        "url,file,retrieved_on\nhttps://x.example/,p.txt,d\nhttps://x.example/,p.txt,d\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="recorded twice"):
        RecordedFetcher(tmp_path)
    manifest.write_text("url,file,retrieved_on\nhttps://x.example/,,d\n", encoding="utf-8")
    with pytest.raises(ValueError, match="needs a url and a file"):
        RecordedFetcher(tmp_path)


NETWORK_MODULES = {
    "socket",
    "ssl",
    "http.client",
    "urllib.request",
    "urllib3",
    "requests",
    "httpx",
    "aiohttp",
}


def _imports(path: Path) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
            found.update(f"{node.module}.{alias.name}" for alias in node.names)
    return found


def test_the_core_imports_no_network_library() -> None:
    offenders = {
        f"{path.relative_to(ROOT)}: {name}"
        for path in (ROOT / "src" / "gsps_fetch").rglob("*.py")
        for name in _imports(path)
        if any(name == m or name.startswith(m + ".") for m in NETWORK_MODULES)
    }
    assert not offenders, sorted(offenders)
