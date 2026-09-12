from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from urllib.parse import SplitResult, parse_qsl, urlencode, urlsplit, urlunsplit

from detrack.patterns import DEFAULT_PATTERNS
from detrack.settings import DEFAULT_SETTINGS, Settings

_DEFAULT_PATTERNS_LOWER: frozenset[str] = frozenset(
    p.lower() for p in DEFAULT_PATTERNS
)


@dataclass
class DetrackResult:
    """Result of cleaning tracking parameters from a URL.

    Attributes:
        url: The cleaned URL with tracking parameters removed.
        parsed_url: The parsed components of the original URL.
        cleaned_params: Query parameters that were kept (not tracking).
        removed_params: Query parameters that were stripped (tracking).
    """

    url: str
    parsed_url: SplitResult
    cleaned_params: dict[str, str]
    removed_params: dict[str, str]


def _filter_pairs(
    query: str,
    patterns: Iterable[str] | None = None,
) -> tuple[list[tuple[str, str]], dict[str, str]]:
    if patterns is not None:
        patterns_set = frozenset(p.lower() for p in patterns)
    else:
        patterns_set = _DEFAULT_PATTERNS_LOWER
    pairs = parse_qsl(query, keep_blank_values=True)
    cleaned: list[tuple[str, str]] = []
    removed: dict[str, str] = {}
    for key, val in pairs:
        if key.lower() in patterns_set:
            removed[key] = val
        else:
            cleaned.append((key, val))
    return cleaned, removed


def clean_query(
    query: str,
    patterns: Iterable[str] | None = None,
    settings: Settings | None = None,
) -> str:
    """Strip tracking parameters from a raw query string.

    Args:
        query: A URL query string (e.g. ``"q=python&utm_source=twitter"``).
        patterns: Parameter names to remove. Defaults to :data:`DEFAULT_PATTERNS`.
            Pass an empty list to keep everything.
        settings: Runtime settings. Uses :data:`DEFAULT_SETTINGS` when ``None``.

    Returns:
        The cleaned query string. If the input is malformed or exceeds
        the configured max length, the original query is returned unchanged.

    Examples::

        >>> from detrack import clean_query
        >>> clean_query("q=python&utm_source=twitter")
        'q=python'

        >>> clean_query("a=1&b=2")  # no tracking params
        'a=1&b=2'

        >>> clean_query("utm_source=x&fbclid=y")  # all stripped
        ''

        >>> clean_query("q=1", patterns=["q"])  # custom patterns
        ''
    """
    settings = settings or DEFAULT_SETTINGS
    try:
        if len(query) > settings.max_query_length:
            return query
        cleaned, _ = _filter_pairs(query, patterns)
        return urlencode(cleaned, doseq=True)
    except Exception:
        return query


def clean(
    url: str,
    patterns: Iterable[str] | None = None,
    settings: Settings | None = None,
) -> DetrackResult:
    """Strip tracking parameters from a full URL.

    Args:
        url: A complete URL (e.g. ``"https://example.com/post?q=1&utm_source=x"``).
        patterns: Parameter names to remove. Defaults to :data:`DEFAULT_PATTERNS`.
            Pass an empty list to keep everything.
        settings: Runtime settings. Uses :data:`DEFAULT_SETTINGS` when ``None``.

    Returns:
        A :class:`DetrackResult` with the cleaned URL, kept parameters,
        and removed parameters. On malformed input, returns the original
        URL unchanged with empty param dicts.

    Examples::

        >>> from detrack import clean
        >>> result = clean("https://example.com/post?q=python&utm_source=twitter")
        >>> result.url
        'https://example.com/post?q=python'

        >>> result.removed_params
        {'utm_source': 'twitter'}

        >>> result.cleaned_params
        {'q': 'python'}

        >>> clean("https://example.com/page").url  # no tracking
        'https://example.com/page'
    """
    settings = settings or DEFAULT_SETTINGS
    if not url or "?" not in url:
        try:
            parsed = urlsplit(url)
        except Exception:
            parsed = urlsplit("")
        return DetrackResult(
            url=url,
            parsed_url=parsed,
            cleaned_params={},
            removed_params={},
        )
    try:
        parsed = urlsplit(url)
        if len(parsed.query) > settings.max_query_length:
            return DetrackResult(
                url=url,
                parsed_url=parsed,
                cleaned_params={},
                removed_params={},
            )
        if not parsed.query:
            return DetrackResult(
                url=url,
                parsed_url=parsed,
                cleaned_params={},
                removed_params={},
            )
        cleaned_pairs, removed = _filter_pairs(parsed.query, patterns)
        cleaned_qs = urlencode(cleaned_pairs, doseq=True)
        cleaned_dict = dict(cleaned_pairs)
        new_url = urlunsplit((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            cleaned_qs,
            parsed.fragment,
        ))
        return DetrackResult(
            url=new_url,
            parsed_url=parsed,
            cleaned_params=cleaned_dict,
            removed_params=removed,
        )
    except Exception:
        return DetrackResult(
            url=url,
            parsed_url=urlsplit(url),
            cleaned_params={},
            removed_params={},
        )
