from detrack import DetrackResult, Settings, clean, clean_query, __version__


def test_clean_basic() -> None:
    result = clean("https://example.com/post?utm_source=twitter&q=python")
    assert result.url == "https://example.com/post?q=python"
    assert result.cleaned_params == {"q": "python"}
    assert result.removed_params == {"utm_source": "twitter"}


def test_clean_multiple_trackers() -> None:
    result = clean("https://example.com?a=1&utm_source=x&b=2&fbclid=y&c=3")
    assert result.url == "https://example.com?a=1&b=2&c=3"
    assert result.cleaned_params == {"a": "1", "b": "2", "c": "3"}
    assert result.removed_params == {"utm_source": "x", "fbclid": "y"}


def test_clean_all_stripped() -> None:
    result = clean("https://example.com?utm_source=x&fbclid=y")
    assert result.url == "https://example.com"
    assert result.cleaned_params == {}
    assert result.removed_params == {"utm_source": "x", "fbclid": "y"}


def test_clean_custom_patterns() -> None:
    result = clean("https://example.com?session=abc123&page=1", patterns=["session"])
    assert result.url == "https://example.com?page=1"
    assert result.cleaned_params == {"page": "1"}
    assert result.removed_params == {"session": "abc123"}


def test_clean_preserves_fragment() -> None:
    result = clean("https://example.com/page?utm_source=x#section")
    assert result.url == "https://example.com/page#section"
    assert result.removed_params == {"utm_source": "x"}


def test_clean_no_query() -> None:
    result = clean("https://example.com/page")
    assert result.url == "https://example.com/page"
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_empty_url() -> None:
    result = clean("")
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_malformed_url() -> None:
    url = "http:///example.com"
    result = clean(url)
    assert result.url == url
    assert result.removed_params == {}


def test_clean_query_basic() -> None:
    result = clean_query("a=1&utm_source=x&b=2")
    assert result == "a=1&b=2"


def test_clean_query_all_stripped() -> None:
    result = clean_query("utm_source=x&fbclid=y")
    assert result == ""


def test_clean_query_empty() -> None:
    assert clean_query("") == ""


def test_clean_query_no_trackers() -> None:
    assert clean_query("a=1&b=2") == "a=1&b=2"


def test_clean_query_custom_patterns() -> None:
    result = clean_query("session=abc&page=1", patterns=["session"])
    assert result == "page=1"


def test_detrack_result_fields() -> None:
    result = clean("https://example.com/p?utm_source=x")
    assert isinstance(result, DetrackResult)
    assert hasattr(result, "url")
    assert hasattr(result, "parsed_url")
    assert hasattr(result, "cleaned_params")
    assert hasattr(result, "removed_params")


def test_clean_query_malformed_returns_input() -> None:
    assert clean_query("%%%") == "%25%25%25="


def test_clean_query_max_length_default() -> None:
    long_query = "a=1&" * 3000  # ~15KB
    assert clean_query(long_query) == long_query


def test_clean_query_max_length_custom() -> None:
    settings = Settings(max_query_length=10)
    assert clean_query("a=1&b=2", settings=settings) == "a=1&b=2"


def test_clean_query_within_custom_limit() -> None:
    settings = Settings(max_query_length=30)
    result = clean_query("q=python&utm_source=x", settings=settings)
    assert result == "q=python"


def test_clean_query_over_custom_limit() -> None:
    settings = Settings(max_query_length=10)
    query = "q=python&utm_source=x"  # 24 chars
    assert clean_query(query, settings=settings) == query


def test_clean_query_empty_patterns() -> None:
    assert clean_query("utm_source=x&q=1", patterns=[]) == "utm_source=x&q=1"


def test_version_exists() -> None:
    assert __version__ == "0.3.0"


def test_clean_with_settings() -> None:
    settings = Settings(max_query_length=30)
    result = clean("https://example.com?q=python&utm_source=x", settings=settings)
    assert result.url == "https://example.com?q=python"
    assert result.removed_params == {"utm_source": "x"}


def test_clean_with_oversized_query() -> None:
    settings = Settings(max_query_length=10)
    long_url = "https://example.com?" + "a=1&" * 3000
    result = clean(long_url, settings=settings)
    assert result.url == long_url
    assert result.removed_params == {}


def test_clean_question_mark_no_query() -> None:
    result = clean("https://example.com?")
    assert result.url == "https://example.com?"
    assert result.cleaned_params == {}
    assert result.removed_params == {}
