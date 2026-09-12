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
    try:
        configure(unknown_field=1)
        assert False, "Should have raised TypeError"
    except TypeError as e:
        assert "unknown_field" in str(e)


def test_clean_query_uses_default_settings() -> None:
    long_query = "a=1&" * 3000
    assert clean_query(long_query) == long_query
