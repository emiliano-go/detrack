"""Strip tracking parameters from URLs. Deterministically. Zero dependencies.

Examples::

    >>> import detrack
    >>> result = detrack.clean("https://example.com?utm_source=x&q=1")
    >>> result.url
    'https://example.com?q=1'

    >>> detrack.clean_url("https://example.com?fbclid=123&q=python")
    'https://example.com?q=python'
"""

from detrack.core import DetrackResult, clean, clean_batch, clean_query, clean_url
from detrack.patterns import DEFAULT_PATTERNS, PREFIXES
from detrack.settings import DEFAULT_SETTINGS, Settings, configure

__version__ = "0.3.0"

__all__ = [
    "clean",
    "clean_batch",
    "clean_query",
    "clean_url",
    "DEFAULT_PATTERNS",
    "DetrackResult",
    "PREFIXES",
    "Settings",
    "DEFAULT_SETTINGS",
    "configure",
    "__version__",
]
