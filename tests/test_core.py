from detrack import (
    PREFIXES,
    DetrackResult,
    Settings,
    __version__,
    clean,
    clean_batch,
    clean_query,
    clean_url,
)


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


def test_prefix_matching_utm() -> None:
    result = clean_query("utm_custom=x&q=1")
    assert result == "q=1"


def test_prefix_matching_mtm() -> None:
    result = clean_query("mtm_custom=x&q=1")
    assert result == "q=1"


def test_prefix_matching_hsa() -> None:
    result = clean_query("hsa_custom=x&q=1")
    assert result == "q=1"


def test_prefix_disabled() -> None:
    settings = Settings(use_prefixes=False)
    result = clean_query("utm_custom=x&q=1", settings=settings)
    assert result == "utm_custom=x&q=1"


def test_prefix_disabled_preserves_explicit_match() -> None:
    settings = Settings(use_prefixes=False)
    result = clean_query("utm_source=x&q=1", settings=settings)
    assert result == "q=1"


def test_custom_patterns_ignore_prefixes() -> None:
    result = clean_query("utm_source=x&q=1", patterns=["utm_source"])
    assert result == "q=1"
    result2 = clean_query("utm_custom=x&q=1", patterns=["utm_source"])
    assert result2 == "utm_custom=x&q=1"


def test_clean_spotify_url() -> None:
    url = "https://open.spotify.com/track/abc?si=xyz&utm_source=copy-link"
    result = clean(url)
    assert "si=" not in result.url
    assert "utm_source" not in result.url
    assert result.removed_params.get("si") == "xyz"
    assert result.removed_params.get("utm_source") == "copy-link"


def test_clean_hubspot_url() -> None:
    url = "https://example.com?hsa_acc=123&hsa_cam=456&q=python"
    result = clean(url)
    assert result.url == "https://example.com?q=python"
    assert "hsa_acc" in result.removed_params
    assert "hsa_cam" in result.removed_params


def test_clean_matomo_url() -> None:
    url = "https://example.com?mtm_campaign=spring&mtm_medium=email&q=1"
    result = clean(url)
    assert result.url == "https://example.com?q=1"


def test_clean_tiktok_url() -> None:
    url = "https://example.com?ttclid=abc123&q=1"
    result = clean(url)
    assert result.url == "https://example.com?q=1"
    assert result.removed_params.get("ttclid") == "abc123"


def test_clean_linkedin_url() -> None:
    url = "https://example.com?li_fat_id=abc123&q=1"
    result = clean(url)
    assert result.url == "https://example.com?q=1"


def test_has_tracking_true() -> None:
    result = clean("https://example.com?utm_source=x&q=1")
    assert result.has_tracking is True


def test_has_tracking_false() -> None:
    result = clean("https://example.com?q=1&page=2")
    assert result.has_tracking is False


def test_has_tracking_empty_url() -> None:
    result = clean("https://example.com")
    assert result.has_tracking is False


def test_has_tracking_all_removed() -> None:
    result = clean("https://example.com?utm_source=x&fbclid=y")
    assert result.has_tracking is True


def test_clean_batch_multiple() -> None:
    urls = [
        "https://example.com?a=1&utm_source=x",
        "https://example.com?fbclid=y&b=2",
        "https://example.com?c=3",
    ]
    results = clean_batch(urls)
    assert len(results) == 3
    assert results[0].url == "https://example.com?a=1"
    assert results[1].url == "https://example.com?b=2"
    assert results[2].url == "https://example.com?c=3"
    assert results[0].has_tracking is True
    assert results[1].has_tracking is True
    assert results[2].has_tracking is False


def test_clean_batch_empty() -> None:
    assert clean_batch([]) == []


def test_clean_batch_with_patterns() -> None:
    urls = [
        "https://example.com?utm_source=x&q=1",
        "https://example.com?session=abc&q=2",
    ]
    results = clean_batch(urls, patterns=["utm_source", "session"])
    assert results[0].url == "https://example.com?q=1"
    assert results[1].url == "https://example.com?q=2"


def test_clean_batch_with_settings() -> None:
    urls = [
        "https://example.com?utm_source=x&q=1",
        "https://example.com?hsa_custom=y&b=2",
    ]
    settings = Settings(use_prefixes=False)
    results = clean_batch(urls, settings=settings)
    assert results[0].url == "https://example.com?q=1"
    assert results[1].url == "https://example.com?hsa_custom=y&b=2"


def test_str_returns_url() -> None:
    result = clean("https://example.com?utm_source=x&q=1")
    assert str(result) == "https://example.com?q=1"
    assert str(result) == result.url


def test_str_in_fstring() -> None:
    result = clean("https://example.com?utm_source=x&q=1")
    assert f"{result}" == "https://example.com?q=1"


def test_repr_no_splitresult() -> None:
    result = clean("https://example.com?utm_source=x&q=1")
    assert "SplitResult" not in repr(result)


def test_repr_shows_url_and_params() -> None:
    result = clean("https://example.com?utm_source=x&q=1")
    r = repr(result)
    assert "DetrackResult(url=" in r
    assert "cleaned_params=" in r
    assert "removed_params=" in r
    assert "https://example.com?q=1" in r
    assert "'utm_source'" in r


def test_iter_unpack() -> None:
    result = clean("https://example.com?utm_source=x&q=1")
    url, cleaned, removed = result
    assert url == "https://example.com?q=1"
    assert cleaned == {"q": "1"}
    assert removed == {"utm_source": "x"}


def test_iter_in_list() -> None:
    result = clean("https://example.com?utm_source=x&q=1")
    assert list(result) == ["https://example.com?q=1", {"q": "1"}, {"utm_source": "x"}]


def test_clean_url_returns_string() -> None:
    result = clean_url("https://example.com?utm_source=x&q=1")
    assert isinstance(result, str)
    assert result == "https://example.com?q=1"


def test_clean_url_strips_tracking() -> None:
    assert clean_url("https://example.com?utm_source=twitter&fbclid=123&q=1") == "https://example.com?q=1"


def test_clean_url_no_tracking() -> None:
    assert clean_url("https://example.com?page=1&q=python") == "https://example.com?page=1&q=python"


def test_clean_url_empty() -> None:
    assert clean_url("") == ""


def test_clean_url_with_patterns() -> None:
    assert clean_url("https://example.com?x=1&q=2", patterns=["x"]) == "https://example.com?q=2"


def test_clean_url_with_settings() -> None:
    settings = Settings(use_prefixes=False)
    url = "https://example.com?utm_custom=x&q=1"
    assert clean_url(url, settings=settings) == url


def test_prefixes_exported() -> None:
    assert "PREFIXES" in __import__("detrack").__all__
    assert isinstance(PREFIXES, tuple)
    assert "utm_" in PREFIXES
    assert len(PREFIXES) == 19
