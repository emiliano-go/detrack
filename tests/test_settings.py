import pytest

from detrack import DEFAULT_SETTINGS, Settings, clean_query, configure


def test_settings_defaults() -> None:
    s = Settings()
    assert s.max_query_length == 8192


def test_settings_custom() -> None:
    s = Settings(max_query_length=1024)
    assert s.max_query_length == 1024


def test_configure_updates_default() -> None:
    original = DEFAULT_SETTINGS.max_query_length
    try:
        configure(max_query_length=4096)
        assert DEFAULT_SETTINGS.max_query_length == 4096
    finally:
        DEFAULT_SETTINGS.max_query_length = original


def test_configure_rejects_unknown_kwarg() -> None:
    with pytest.raises(TypeError, match="unknown_field"):
        configure(unknown_field=1)


def test_clean_query_uses_default_settings() -> None:
    long_query = "a=1&" * 3000
    assert clean_query(long_query) == long_query


def test_settings_max_query_length_zero_raises() -> None:
    with pytest.raises(ValueError, match=">= 1"):
        Settings(max_query_length=0)


def test_settings_max_query_length_negative_raises() -> None:
    with pytest.raises(ValueError, match=">= 1"):
        Settings(max_query_length=-1)


def test_settings_max_query_length_string_raises() -> None:
    with pytest.raises(TypeError, match="int"):
        Settings(max_query_length="abc")  # type: ignore[arg-type]


def test_settings_use_prefixes_string_raises() -> None:
    with pytest.raises(TypeError, match="bool"):
        Settings(use_prefixes="yes")  # type: ignore[arg-type]


def test_settings_use_prefixes_int_raises() -> None:
    with pytest.raises(TypeError, match="bool"):
        Settings(use_prefixes=1)  # type: ignore[arg-type]


def test_settings_valid_use_prefixes_true() -> None:
    s = Settings(use_prefixes=True)
    assert s.use_prefixes is True


def test_settings_valid_use_prefixes_false() -> None:
    s = Settings(use_prefixes=False)
    assert s.use_prefixes is False
