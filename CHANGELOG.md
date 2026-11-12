# Changelog

All notable changes are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Fetcher contract (phase 1 of 7): the `Fetcher` interface, `FetchRequest` and
  `FetchResult` with a SHA-256 receipt that is stable across line endings, and
  `RecordedFetcher`, which replays saved pages with no network. A missing page is a 404
  result, not an exception; a recording cannot name files outside its folder.
- A test that fails if any core module imports a network library.
- Project scaffold: packaging, strict typing, lint, tests and CI on Python 3.11 to 3.13.
