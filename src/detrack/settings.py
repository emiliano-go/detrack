from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any


@dataclass
class Settings:
    """Runtime configuration for detrack.

    Attributes:
        max_query_length: Maximum query string length in characters.
            Longer queries are returned unchanged to prevent abuse.
        use_prefixes: When True, strip params matching known prefixes
            (``utm_*``, ``mtm_*``, ``hsa_*``, ``pk_*``, etc.) even if
            not listed explicitly in the pattern list.

    Raises:
        TypeError: If ``max_query_length`` is not ``int`` or
            ``use_prefixes`` is not ``bool``.
        ValueError: If ``max_query_length < 1``.

    Examples::

        >>> Settings()  # defaults
        Settings(max_query_length=8192, use_prefixes=True)

        >>> Settings(max_query_length=4096, use_prefixes=False)
        Settings(max_query_length=4096, use_prefixes=False)

        >>> from detrack import clean
        >>> result = clean("https://example.com?q=1",
        ...     settings=Settings(use_prefixes=False))
        >>> result.url
        'https://example.com?q=1'
    """

    max_query_length: int = 8192
    use_prefixes: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.max_query_length, int):
            raise TypeError(
                f"max_query_length must be int, "
                f"got {type(self.max_query_length).__name__}"
            )
        if self.max_query_length < 1:
            raise ValueError(
                f"max_query_length must be >= 1, got {self.max_query_length}"
            )
        if not isinstance(self.use_prefixes, bool):
            raise TypeError(
                f"use_prefixes must be bool, got {type(self.use_prefixes).__name__}"
            )


DEFAULT_SETTINGS = Settings()
"""Global default settings. Modify with :func:`configure`."""


def configure(**kwargs: Any) -> None:
    """Update global settings. Only specified fields are changed.

    Args:
        **kwargs: Settings fields to update (e.g. ``max_query_length=16384``).

    Raises:
        TypeError: For unknown keyword arguments or type mismatches.

    Examples::

        >>> from detrack import configure, DEFAULT_SETTINGS
        >>> configure(max_query_length=16384)
        >>> DEFAULT_SETTINGS.max_query_length
        16384

        >>> configure(use_prefixes=False)
        >>> DEFAULT_SETTINGS.use_prefixes
        False

        >>> configure(max_query_length=8192, use_prefixes=True)  # reset
    """
    for key in kwargs:
        if not hasattr(DEFAULT_SETTINGS, key):
            raise TypeError(
                f"configure() got an unexpected keyword argument '{key}'"
            )
    merged = {
        f.name: getattr(DEFAULT_SETTINGS, f.name)
        for f in fields(DEFAULT_SETTINGS)
    }
    merged.update(kwargs)
    new = Settings(**merged)
    for f in fields(new):
        object.__setattr__(DEFAULT_SETTINGS, f.name, getattr(new, f.name))
