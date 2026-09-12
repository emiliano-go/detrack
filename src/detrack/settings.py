from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Settings:
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


def configure(**kwargs: Any) -> None:
    for key, value in kwargs.items():
        if not hasattr(DEFAULT_SETTINGS, key):
            raise TypeError(f"configure() got an unexpected keyword argument '{key}'")
        setattr(DEFAULT_SETTINGS, key, value)
