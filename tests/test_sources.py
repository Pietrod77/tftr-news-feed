from sources import SOURCES


def test_sources_has_exactly_five_entries():
    assert len(SOURCES) == 5


def test_every_source_has_name_and_https_url():
    for source in SOURCES:
        assert source["name"]
        assert source["url"].startswith("https://")


def test_source_urls_are_unique():
    urls = [source["url"] for source in SOURCES]
    assert len(urls) == len(set(urls))
