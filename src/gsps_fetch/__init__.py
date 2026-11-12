"""gsps-fetch: safe, logged, policy-checked page fetching for the GSPS provenance engine.

The core never opens a URL itself. A fetcher is plugged in from outside, and every
result carries the gate it came through and a receipt of what it returned.
"""

__version__ = "0.1.0"
