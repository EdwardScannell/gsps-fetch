# Security

The gsps-fetch core opens no URLs and imports no network library. Fetchers that open
pages are plugged in from outside.

Design choices that matter for safety:

- A recording's manifest may only name files inside the recording folder; a path that
  escapes it is refused when the recording is loaded.
- A page refused by a gate or by policy is never opened through another route.
- No secrets are read. The optional HTTP adapter (roadmap phase 6) will take no
  credentials.

To report a vulnerability, open a private security advisory on the repository rather than
a public issue.
