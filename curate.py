import datetime
import json
import os

import feedparser

from filters import passes_filter
from rewrite import rewrite_item
from sources import SOURCES

USED_ITEMS_PATH = os.path.join(os.path.dirname(__file__), "used_items.json")
FEED_PATH = os.path.join(os.path.dirname(__file__), "feed.json")
WINDOW_SIZE = 5
MAX_NEW_PER_RUN = 2


def load_used_items(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def fetch_candidates(sources):
    candidates = []
    for source in sources:
        parsed = feedparser.parse(source["url"])
        for entry in parsed.entries:
            candidates.append({
                "url": entry.get("link", ""),
                "source": source["name"],
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
            })
    return candidates


def select_new_items(candidates, used_urls, max_new=MAX_NEW_PER_RUN):
    selected = []
    seen = set()
    for candidate in candidates:
        url = candidate["url"]
        if not url or url in used_urls or url in seen:
            continue
        if not passes_filter(candidate["title"], candidate["summary"]):
            continue
        selected.append(candidate)
        seen.add(url)
        if len(selected) >= max_new:
            break
    return selected


def build_feed(used_items, window=WINDOW_SIZE):
    return used_items[-window:]


def main():
    import anthropic

    import config

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    used_items = load_used_items(USED_ITEMS_PATH)
    used_urls = {item["url"] for item in used_items}

    candidates = fetch_candidates(SOURCES)
    new_items = select_new_items(candidates, used_urls)

    today = datetime.date.today().isoformat()
    for item in new_items:
        rewritten = rewrite_item(client, item["source"], item["title"], item["summary"])
        used_items.append({
            "url": item["url"],
            "source": item["source"],
            "headline": rewritten["headline"],
            "blurb": rewritten["blurb"],
            "published": item["published"],
            "added": today,
        })

    save_json(USED_ITEMS_PATH, used_items)
    save_json(FEED_PATH, {
        "updated": datetime.datetime.now().isoformat(),
        "items": build_feed(used_items),
    })


if __name__ == "__main__":
    main()
