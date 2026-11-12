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

## Status

Early. The fetcher is being built in seven phases; see [`ROADMAP.md`](ROADMAP.md).

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
