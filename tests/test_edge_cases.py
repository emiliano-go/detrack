from detrack import clean, clean_query
from detrack.settings import Settings


def test_case_insensitivity_utm() -> None:
    for url in [
        "https://example.com?utm_source=x&q=1",
        "https://example.com?UTM_SOURCE=x&q=1",
        "https://example.com?Utm_Source=x&q=1",
        "https://example.com?utm_SOURCE=x&q=1",
    ]:
        result = clean(url)
        assert result.url == "https://example.com?q=1", f"Failed for {url}"
        assert result.has_tracking


def test_case_insensitivity_fbclid() -> None:
    for url in [
        "https://example.com?fbclid=x&q=1",
        "https://example.com?FBCLID=x&q=1",
        "https://example.com?Fbclid=x&q=1",
    ]:
        result = clean(url)
        assert result.url == "https://example.com?q=1", f"Failed for {url}"


def test_empty_values_preserved_for_non_tracking() -> None:
    result = clean("https://example.com?a=&b=2")
    assert result.url == "https://example.com?a=&b=2"
    assert result.removed_params == {}


def test_empty_values_removed_for_tracking() -> None:
    result = clean("https://example.com?utm_source=&b=2")
    assert result.url == "https://example.com?b=2"
    assert result.removed_params == {"utm_source": ""}


def test_duplicate_params_all_removed() -> None:
    result = clean("https://example.com?utm_source=x&utm_source=y&a=1")
    assert result.url == "https://example.com?a=1"
    assert result.removed_params == {"utm_source": "y"}


def test_url_without_scheme() -> None:
    result = clean("//example.com/page?utm_source=x")
    assert "utm_source" not in result.url


def test_url_with_port() -> None:
    result = clean("https://example.com:8080/page?utm_source=x&q=1")
    assert result.url == "https://example.com:8080/page?q=1"


def test_url_with_auth() -> None:
    result = clean("https://user:pass@example.com/page?utm_source=x&q=1")
    assert result.url == "https://user:pass@example.com/page?q=1"


def test_only_tracking_params_different_cases() -> None:
    result = clean("https://example.com?UTM_CAMPAIGN=spring&utm_medium=email&q=1")
    assert result.url == "https://example.com?q=1"


def test_no_changes_with_no_tracking() -> None:
    url = "https://example.com/search?q=python&page=2"
    result = clean(url)
    assert result.url == url
    assert result.cleaned_params == {"q": "python", "page": "2"}
    assert result.removed_params == {}


def test_query_only_function_with_mixed() -> None:
    assert clean_query("a=1&utm_source=x&b=2") == "a=1&b=2"


def test_query_only_all_tracking() -> None:
    assert clean_query("utm_source=x&fbclid=y") == ""


def test_query_only_empty() -> None:
    assert clean_query("") == ""


def test_query_only_no_tracking() -> None:
    assert clean_query("a=1&b=2") == "a=1&b=2"


def test_clean_none_returns_empty() -> None:
    result = clean(None)  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_true_returns_empty() -> None:
    result = clean(True)  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_int_returns_empty() -> None:
    result = clean(123)  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_list_returns_empty() -> None:
    result = clean([])  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_float_returns_empty() -> None:
    result = clean(3.14)  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_dict_returns_empty() -> None:
    result = clean({})  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_set_returns_empty() -> None:
    result = clean(set())  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_bytes_returns_empty() -> None:
    result = clean(b"https://example.com")  # type: ignore[arg-type]
    assert result.url == ""
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_clean_query_none_returns_empty() -> None:
    assert clean_query(None) == ""  # type: ignore[arg-type]


def test_clean_query_true_returns_empty() -> None:
    assert clean_query(True) == ""  # type: ignore[arg-type]


def test_clean_query_int_returns_empty() -> None:
    assert clean_query(123) == ""  # type: ignore[arg-type]


def test_clean_query_list_returns_empty() -> None:
    assert clean_query([]) == ""  # type: ignore[arg-type]


def test_clean_query_float_returns_empty() -> None:
    assert clean_query(3.14) == ""  # type: ignore[arg-type]


def test_clean_query_dict_returns_empty() -> None:
    assert clean_query({}) == ""  # type: ignore[arg-type]


def test_clean_query_set_returns_empty() -> None:
    assert clean_query(set()) == ""  # type: ignore[arg-type]


def test_clean_query_bytes_returns_empty() -> None:
    assert clean_query(b"q=1") == ""  # type: ignore[arg-type]


def test_url_with_fragment_only() -> None:
    result = clean("https://example.com#section")
    assert result.url == "https://example.com#section"
    assert result.cleaned_params == {}
    assert result.removed_params == {}


def test_url_with_empty_fragment() -> None:
    result = clean("https://example.com?q=1#")
    assert result.url == "https://example.com?q=1"


def test_url_double_question_mark() -> None:
    result = clean("https://example.com??q=1")
    assert result.cleaned_params == {"?q": "1"}


def test_url_trailing_ampersand() -> None:
    result = clean("https://example.com?q=1&")
    assert result.url == "https://example.com?q=1"


def test_url_only_ampersands() -> None:
    result = clean("https://example.com?&&&")
    assert result.url == "https://example.com"


def test_url_question_mark_only() -> None:
    result = clean("https://example.com?")
    assert result.url == "https://example.com?"


def test_url_with_encoded_ampersand_in_value() -> None:
    result = clean("https://example.com?q=a%26b&utm_source=x")
    assert result.url == "https://example.com?q=a%26b"
    assert result.cleaned_params == {"q": "a&b"}


def test_url_with_unicode_in_value() -> None:
    result = clean("https://example.com?q=%E4%B8%AD%E6%96%87&utm_source=x")
    assert "q=" in result.url
    assert "utm_source" not in result.url


def test_url_with_special_chars_in_value() -> None:
    result = clean("https://example.com?q=hello+world%21&utm_source=x")
    assert "q=" in result.url


def test_very_long_url_within_limit() -> None:
    url = "https://example.com?" + "&".join(f"param{i}=value{i}" for i in range(100))
    result = clean(url)
    assert result.url == url


def test_1000_params_all_clean() -> None:
    qs = "&".join(f"p{i}=v{i}" for i in range(1000))
    url = f"https://example.com?{qs}"
    result = clean(url, settings=Settings(max_query_length=20000))
    assert result.url == url
    assert len(result.cleaned_params) == 1000


def test_1000_params_with_tracker() -> None:
    qs = "&".join(f"p{i}=v{i}" for i in range(1000))
    url = f"https://example.com?{qs}&utm_source=x"
    result = clean(url, settings=Settings(max_query_length=20000))
    assert "utm_source" not in result.url
    assert len(result.cleaned_params) == 1000
