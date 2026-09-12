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
