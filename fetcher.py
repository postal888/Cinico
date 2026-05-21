import feedparser

FEEDS = [
    "https://hnrss.org/frontpage",
    "https://feeds.reuters.com/reuters/businessNews",
    "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
]

feedparser.USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_news(max_items: int = 5) -> list[dict]:
    items = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue
        if getattr(feed, "status", 200) >= 400:
            continue
        for entry in feed.entries[:3]:
            title = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            link = entry.get("link", "")
            if title:
                items.append({"title": title, "summary": summary[:300], "link": link})
        if len(items) >= max_items * 2:
            break

    # deduplicate by title prefix
    seen = set()
    unique = []
    for item in items:
        key = item["title"][:40].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique[:max_items]
