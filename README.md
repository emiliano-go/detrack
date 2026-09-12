<h1 align="center">detrack</h1>

<p align="center">
  <strong>Strip tracking parameters from URLs. Deterministically. Zero dependencies.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/detrack/"><img src="https://img.shields.io/pypi/v/detrack?style=flat-square&color=blue" alt="PyPI"></a>
  <img src="https://img.shields.io/pypi/pyversions/detrack?style=flat-square" alt="Python">
  <img src="https://img.shields.io/pypi/l/detrack?style=flat-square&color=green" alt="License">
  <img src="https://img.shields.io/badge/dependencies-none-brightgreen?style=flat-square" alt="no dependencies">
</p>

## Install

```bash
pip install detrack
```

## Quick start

```python
import detrack

url = "https://example.com/post?utm_source=twitter&q=python&fbclid=123"
result = detrack.clean(url)

print(result.url)
# "https://example.com/post?q=python"

print(result.removed_params)
# {"utm_source": "twitter", "fbclid": "123"}

print(result.cleaned_params)
# {"q": "python"}
```

## Why detrack?

Other URL cleaners do too much (host remapping, site-specific rules, semantic rewriting), while `detrack` does one thing and does it well: remove tracking parameters.

This makes `detrack` predictable, testable, and trivial to integrate.

## Ecosystem

`detrack` is the shared cleaning layer for the [seoslug](https://github.com/emiliano-gandini-outeda/seoslug) (SEO metadata) and [tagurl](https://github.com/emiliano-gandini-outeda/tagurl) (semantic tagging) libraries.

## Configuration

`detrack` ships with sensible defaults. Override them globally with `configure()`, or per-call with a `Settings` object.

### Global configuration

```python
from detrack import configure

# Raise the query length limit to 16KB
configure(max_query_length=16384)
```

### Per-call override

```python
from detrack import Settings, clean_query

# This call uses a 2KB limit, ignoring the global setting
clean_query(query, settings=Settings(max_query_length=2048))
```

### `Settings`

```python
@dataclass
class Settings:
    max_query_length: int = 8192  # queries longer than this are returned unchanged
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_query_length` | `int` | `8192` | Maximum query string length (in characters). Longer queries are returned unchanged to prevent abuse. |

---

## Examples

### Basic

```python
>>> detrack.clean("https://example.com?utm_source=twitter&q=python")
DetrackResult(url="https://example.com?q=python", cleaned_params={"q": "python"},
              removed_params={"utm_source": "twitter"})
```

### Multiple trackers stripped

```python
>>> detrack.clean("https://example.com?a=1&utm_source=x&b=2&fbclid=y&c=3")
DetrackResult(url="https://example.com?a=1&b=2&c=3",
              cleaned_params={"a": "1", "b": "2", "c": "3"},
              removed_params={"utm_source": "x", "fbclid": "y"})
```

### All params stripped (query removed entirely)

```python
>>> detrack.clean("https://example.com?utm_source=x&fbclid=y")
DetrackResult(url="https://example.com",
              cleaned_params={},
              removed_params={"utm_source": "x", "fbclid": "y"})
```

### Custom patterns

```python
>>> detrack.clean("https://example.com?session=abc123&page=1", patterns=["session"])
DetrackResult(url="https://example.com?page=1",
              cleaned_params={"page": "1"},
              removed_params={"session": "abc123"})
```

### Query string only

```python
>>> detrack.clean_query("a=1&utm_source=x&b=2")
"a=1&b=2"

>>> detrack.clean_query("utm_source=x&fbclid=y")
""
```

## API

### `detrack.clean(url, patterns=None, settings=None)`

Strip tracking parameters from a full URL.

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | Any URL string |
| `patterns` | `Iterable[str] \| None` | Optional param names to strip (defaults to `DEFAULT_PATTERNS`) |
| `settings` | `Settings \| None` | Optional per-call settings override (defaults to `DEFAULT_SETTINGS`) |

**Returns:** [`DetrackResult`](#detrackresult) -> dataclass with cleaned URL and metadata.

**Raises:** Nothing -> pure function, no exceptions.
Malformed URLs pass through unchanged. Queries exceeding `max_query_length` are returned unchanged.

---

### `detrack.clean_query(query, patterns=None, settings=None)`

Strip tracking parameters from a query string only.

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | URL query string, e.g. `"a=1&utm_source=x&b=2"` |
| `patterns` | `Iterable[str] \| None` | Optional param names to strip |
| `settings` | `Settings \| None` | Optional per-call settings override (defaults to `DEFAULT_SETTINGS`) |

**Returns:** `str` -> cleaned query string. Returns the input unchanged if it's malformed or exceeds `max_query_length`.

---

### `detrack.configure(**kwargs)`

Update global settings. Only specified fields are changed.

```python
from detrack import configure

configure(max_query_length=16384)
```

**Raises:** `TypeError` for unknown keyword arguments.

---

### `detrack.DEFAULT_PATTERNS`

```python
frozenset[str]  # 60+ common tracking parameters
```

Covers UTM parameters, social tracking (`fbclid`, `ref`, `si`), marketing IDs
(`gclid`, `msclkid`, `wbraid`), analytics (`_ga`, `_gl`), cache busters
(`cb`, `rand`, `timestamp`), session IDs (`sid`, `phpsessid`), and redirect
params. Pass a custom `patterns` list to `clean()` to override.

---

### `DetrackResult`

```python
@dataclass
class DetrackResult:
    url: str                       # Cleaned URL
    parsed_url: SplitResult        # urllib.parse result (for further processing)
    cleaned_params: dict[str, str] # Parameters that remain
    removed_params: dict[str, str] # Stripped parameters + their original values
```

`removed_params` preserves the original values so you can log what was stripped
for analytics, debugging, or compliance.

## Features

- **60+ default patterns**: UTM, social, marketing, analytics, cache busters, session, redirect
- **Case-insensitive matching**: `UTM_SOURCE`, `Utm_Source`, and `utm_source` are all stripped
- **Zero dependencies**: uses only `urllib.parse` from the Python standard library
- **Deterministic**: same input always yields the same output, across all systems
- **Pure functions**: no state, no I/O, no random numbers, no exceptions
- **Metadata returned**: `removed_params` tells you exactly what was stripped and its original value
- **Configurable length guard**: protects against oversized queries (8KB default, adjustable)

---

See MIT [LICENSE](LICENSE).
