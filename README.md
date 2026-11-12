# gsps-fetch

**Safe, logged, policy-checked page fetching for the [GSPS](https://github.com/EdwardScannell/gsps)
provenance engine.**

GSPS grades every external figure by walking it to its owner's primary source. gsps-fetch
makes *how a page was opened* a typed, recorded step: every fetch names the gate it came
through and carries a receipt of exactly what it returned, and a page that policy refuses
is never opened at all.

[![CI](https://github.com/EdwardScannell/gsps-fetch/actions/workflows/ci.yml/badge.svg)](https://github.com/EdwardScannell/gsps-fetch/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)

## Why

A fact-check is only as good as its record of where each page came from. The usual
failures are quiet ones:

| Failure | What gsps-fetch does |
|---|---|
| Nobody can say which version of a page a figure came from | Every result carries a **SHA-256 receipt** of the text it returned. |
| A blocked or login-walled page gets "fetched anyway" through a mirror or cache | A refused page is **never routed around**; it becomes a follow-up for a person. |
| A failed fetch silently disappears | Failures are **results, not exceptions**, so they can be logged and followed up. |
| Fetching code creeps into the core and makes it untestable | The core **imports no network library**, and a test enforces it. |

## Who it's for

Anyone using GSPS, or building their own fact-checking or research pipeline, who needs to
prove where each page came from and that no page was opened against policy: analysts,
researchers, editors and the people who review their work.

## Built with

- **Python 3.11+**, fully typed (`mypy --strict`)
- **pydantic** for request and result records; the **gsps** package for the shared gate
  vocabulary
- **pytest** with coverage, **ruff**, **GitHub Actions** CI on 3.11 to 3.13
- No network code in the core. Fetchers that open pages plug in from outside.

## Install

```bash
pip install -e ".[dev]"     # from a clone; pulls gsps from GitHub
make check                  # lint, strict types, tests with coverage
```

## Quick start

Replay a saved page (no network) and get it back with its receipt:

```python
from pathlib import Path

from gsps.vocab.values import Gate
from gsps_fetch import FetchRequest, RecordedFetcher

fetcher = RecordedFetcher(Path("tests/fixtures/recorded"))
result = fetcher.fetch(
    FetchRequest(url="https://stats.example.gov/release/payrolls-2026-10", gate=Gate.PASTE)
)
print(result.ok, result.gate.value, result.retrieved_on, result.sha256[:12])
# True paste 2026-11-07 <first 12 hex characters of the receipt>

missing = fetcher.fetch(FetchRequest(url="https://stats.example.gov/nope", gate=Gate.PASTE))
print(missing.ok, missing.gate.value, missing.detail)
# False 404 not in this recording
```

A recording is a folder with a `MANIFEST.csv` (`url`, `file`, `retrieved_on`, optional
`final_url`) and the saved text files it names. Any fetcher you write implements the same
`Fetcher` interface: one `fetch(request) -> result` method and a `name`.

## Layout

```
src/gsps_fetch/
  protocol.py    Fetcher interface, FetchRequest, FetchResult, content_hash
  recorded.py    RecordedFetcher: replays saved pages, never opens a URL
tests/
  fixtures/recorded/   a synthetic recording
```

## Status

Phase 1 of 7 is done. See [`ROADMAP.md`](ROADMAP.md) for what comes next; plans are also
tracked in the repository's issues.

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
