from detrack import DEFAULT_PATTERNS
from detrack.patterns import _PREFIXES


def test_default_patterns_count() -> None:
    assert len(DEFAULT_PATTERNS) >= 200, (
        f"DEFAULT_PATTERNS has {len(DEFAULT_PATTERNS)} items, expected >= 200"
    )


def test_utm_params_present() -> None:
    utm = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
           "utm_id", "utm_cid", "utm_reader", "utm_viz", "utm_pubreferrer",
           "utm_nooverride"}
    assert utm.issubset(DEFAULT_PATTERNS), (
        f"Missing UTM params: {utm - DEFAULT_PATTERNS}"
    )


def test_social_params_present() -> None:
    social = {"fbclid", "ref", "source", "si", "sns", "social", "origin"}
    assert social.issubset(DEFAULT_PATTERNS), (
        f"Missing social params: {social - DEFAULT_PATTERNS}"
    )


def test_marketing_params_present() -> None:
    marketing = {"gclid", "gclsrc", "dclid", "msclkid", "wbraid", "gbraid",
                 "mc_cid", "mc_eid", "trk", "vero_conv", "vero_id",
                 "email", "recipient", "campaign_id", "newsletter", "mbid"}
    assert marketing.issubset(DEFAULT_PATTERNS), (
        f"Missing marketing params: {marketing - DEFAULT_PATTERNS}"
    )


def test_analytics_params_present() -> None:
    analytics = {"_ga", "_gl", "_ke", "_hsenc"}
    assert analytics.issubset(DEFAULT_PATTERNS), (
        f"Missing analytics params: {analytics - DEFAULT_PATTERNS}"
    )


def test_cache_busters_present() -> None:
    cache = {"_", "cb", "cache", "nocache", "rand", "random", "r", "ts", "_t",
             "timestamp"}
    assert cache.issubset(DEFAULT_PATTERNS), (
        f"Missing cache buster params: {cache - DEFAULT_PATTERNS}"
    )


def test_session_params_present() -> None:
    session = {"session_id", "sid", "phpsessid", "jsessionid", "view_id", "visit_id"}
    assert session.issubset(DEFAULT_PATTERNS), (
        f"Missing session params: {session - DEFAULT_PATTERNS}"
    )


def test_redirect_params_present() -> None:
    redirect = {"redirect_to", "return_to", "next", "continue"}
    assert redirect.issubset(DEFAULT_PATTERNS), (
        f"Missing redirect params: {redirect - DEFAULT_PATTERNS}"
    )


def test_hubspot_params_present() -> None:
    hubspot = {"_hsenc", "_hsmi", "__hsfp", "__hssc", "__hstc",
               "hsa_acc", "hsa_ad", "hsa_cam", "hsa_kw", "hsCtaTracking"}
    assert hubspot.issubset(DEFAULT_PATTERNS), (
        f"Missing HubSpot params: {hubspot - DEFAULT_PATTERNS}"
    )


def test_matomo_params_present() -> None:
    matomo = {"mtm_campaign", "mtm_medium", "mtm_source", "pk_campaign",
              "pk_medium", "pk_source"}
    assert matomo.issubset(DEFAULT_PATTERNS), (
        f"Missing Matomo params: {matomo - DEFAULT_PATTERNS}"
    )


def test_click_ids_present() -> None:
    ids = {"fbclid", "gclid", "msclkid", "ttclid", "twclid", "li_fat_id",
           "sccid", "qclid", "epik"}
    assert ids.issubset(DEFAULT_PATTERNS), (
        f"Missing click IDs: {ids - DEFAULT_PATTERNS}"
    )


def test_spotify_params_present() -> None:
    spotify = {"si", "nd", "dl_branch", "context"}
    assert spotify.issubset(DEFAULT_PATTERNS), (
        f"Missing Spotify params: {spotify - DEFAULT_PATTERNS}"
    )


def test_adjust_params_present() -> None:
    adjust = {"adj_t", "adj_campaign", "gps_adid", "adjust_campaign"}
    assert adjust.issubset(DEFAULT_PATTERNS), (
        f"Missing Adjust params: {adjust - DEFAULT_PATTERNS}"
    )


def test_appsflyer_params_present() -> None:
    af = {"af_xp", "af_ad", "af_adset", "pid"}
    assert af.issubset(DEFAULT_PATTERNS), (
        f"Missing AppsFlyer params: {af - DEFAULT_PATTERNS}"
    )


def test_prefixes_exist() -> None:
    assert len(_PREFIXES) > 0
    assert "utm_" in _PREFIXES
    assert "mtm_" in _PREFIXES


def test_no_duplicates() -> None:
    lower = [p.lower() for p in DEFAULT_PATTERNS]
    assert len(lower) == len(set(lower)), "DEFAULT_PATTERNS contains duplicates"
