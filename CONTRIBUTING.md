# Contributing

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
make install
make check           # lint, strict types, tests with coverage (must stay >= 90%)
```

## The rules for changes

1. **The core never opens a URL.** Code that touches the network lives in an adapter
   outside the core package. A test fails if a core module imports a network library.
2. **A refused page is never routed around.** No mirrors, caches, scrapers or alternate
   browsers for a page that a gate or the policy refused.
3. **Failures are results.** A fetcher returns a result with a failing gate; it does not
   raise for an ordinary failure, so every attempt can be logged.
4. **Every bug gets a regression test first**, named after the failure it guards against.
5. **Keep the public API typed.** `mypy --strict` must pass.

## Pull requests

- One topic per PR, with a test that fails before the change and passes after.
- Update `CHANGELOG.md` under an `Unreleased` heading, and tick the phase in `ROADMAP.md`
  when it is complete.

## Fixtures and data

Recorded pages in fixtures are synthetic. Do not add personal data, private documents or
pages you do not have the right to publish.
