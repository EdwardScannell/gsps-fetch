"""gsps-fetch: safe, logged, policy-checked page fetching for the GSPS provenance engine.

The core never opens a URL itself. A fetcher is plugged in from outside (a person
pasting text, a replay of saved pages, or later an adapter), and every result carries
the gate it came through and a receipt of what it returned.
"""

from gsps_fetch.protocol import Fetcher, FetchRequest, FetchResult, content_hash
from gsps_fetch.recorded import RecordedFetcher

__version__ = "0.1.0"

__all__ = [
    "FetchRequest",
    "FetchResult",
    "Fetcher",
    "RecordedFetcher",
    "__version__",
    "content_hash",
]
