# Roadmap

gsps-fetch is built in seven phases. Each phase lands as its own pull request with tests,
and CI stays green on every commit.

1. [x] **Fetcher interface and replay fetcher.** The `Fetcher` contract, request and result
   records with a SHA-256 receipt, and a fetcher that replays saved pages with no network.
2. [ ] **Source policy.** Dated, versioned allow and block lists; domain resolution
   (subdomains, `www.`); link shorteners refused until expanded; open and closed modes;
   the blocklist always beats the allowlist; every decision records its policy version.
3. [ ] **Guarded fetching.** Wrap any fetcher and refuse before calling it when the gate is
   not cleared, a chained link's parent was not fetched, or policy refuses. Size gate.
   Failures become GSPS follow-up items.
4. [ ] **Fetch log in walk provenance.** A dated fetch log with one row per attempt,
   refusals included; GSPS ingest cites the fetch behind each value.
5. [ ] **Fetch commands.** A manual fetcher for pasted text, and `fetch-check` and `fetch`
   commands.
6. [ ] **Optional HTTP adapter.** Outside the core: robots.txt, user agent, timeouts, rate
   limit. Tested against a local server only.
7. [ ] **Redirects, syndication, reusable policy.** Resolve redirects and canonical URLs
   before the policy check; credit syndicated stories to the original publisher; make the
   policy importable on its own.

## Never

- Scraping, crawling, login, paywall or CAPTCHA handling.
- Routing around a refused page through a mirror, cache or another browser.
