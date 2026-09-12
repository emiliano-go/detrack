from dataclasses import dataclass


@dataclass
class Settings:
    max_query_length: int = 8192


DEFAULT_SETTINGS = Settings()


def configure(**kwargs: int) -> None:
    for key, value in kwargs.items():
        if not hasattr(DEFAULT_SETTINGS, key):
            raise TypeError(f"configure() got an unexpected keyword argument '{key}'")
        setattr(DEFAULT_SETTINGS, key, value)
