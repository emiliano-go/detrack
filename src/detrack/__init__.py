from detrack.core import DetrackResult, clean, clean_batch, clean_query
from detrack.patterns import DEFAULT_PATTERNS
from detrack.settings import DEFAULT_SETTINGS, Settings, configure

__version__ = "0.3.0"

__all__ = [
    "clean",
    "clean_batch",
    "clean_query",
    "DEFAULT_PATTERNS",
    "DetrackResult",
    "Settings",
    "DEFAULT_SETTINGS",
    "configure",
    "__version__",
]
