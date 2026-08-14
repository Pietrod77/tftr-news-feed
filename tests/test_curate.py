# tests/test_curate.py
from curate import build_feed, fetch_candidates, select_new_items


class _FakeEntry(dict):
    def get(self, key, default=None):
        return dict.get(self, key, default)


class _FakeParsed:
    def __init__(self, entries):
        self.entries = entries


def test_fetch_candidates_maps_feed_entries(monkeypatch):
    import curate

    def fake_parse(url):
        return _FakeParsed([
            _FakeEntry(link="https://a.com/1", title="A Title", summary="A summary", published="2026-08-13"),
        ])

    monkeypatch.setattr(curate.feedparser, "parse", fake_parse)

    result = fetch_candidates([{"name": "WWD", "url": "https://wwd.com/feed/"}])

    assert result == [{
        "url": "https://a.com/1",
        "source": "WWD",
        "title": "A Title",
        "summary": "A summary",
        "published": "2026-08-13",
    }]


def test_select_new_items_filters_dedupes_and_caps():
    candidates = [
        {"url": "https://a.com/1", "source": "WWD", "title": "New Biofabricated Leather Material", "summary": "Grown from mycelium.", "published": "2026-08-13"},
        {"url": "https://a.com/1", "source": "WWD", "title": "New Biofabricated Leather Material", "summary": "Grown from mycelium.", "published": "2026-08-13"},
        {"url": "https://a.com/2", "source": "WWD", "title": "Celebrity Wore Recycled Denim on Red Carpet", "summary": "", "published": "2026-08-13"},
        {"url": "https://a.com/3", "source": "BoF", "title": "New Weaving Technique Cuts Textile Waste", "summary": "Mill trials new loom pattern.", "published": "2026-08-13"},
        {"url": "https://a.com/4", "source": "Just Style", "title": "Factory Adopts 3D Print Manufacturing", "summary": "Reduces sample lead time.", "published": "2026-08-13"},
    ]

    result = select_new_items(candidates, used_urls=set(), max_new=2)

    assert [item["url"] for item in result] == ["https://a.com/1", "https://a.com/3"]


def test_select_new_items_skips_already_used():
    candidates = [
        {"url": "https://a.com/1", "source": "WWD", "title": "New Weaving Technique", "summary": "materials innovation", "published": "2026-08-13"},
    ]

    result = select_new_items(candidates, used_urls={"https://a.com/1"}, max_new=2)

    assert result == []


def test_build_feed_returns_last_window_items():
    used_items = [{"url": f"https://a.com/{i}"} for i in range(8)]

    result = build_feed(used_items, window=5)

    assert [item["url"] for item in result] == [
        "https://a.com/3", "https://a.com/4", "https://a.com/5",
        "https://a.com/6", "https://a.com/7",
    ]
