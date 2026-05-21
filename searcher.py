import feedparser
import re

NITTER_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.1d4.us",
    "https://nitter.net",
]

QUERIES = [
    "startup funding round",
    "pitch deck investors",
    "venture capital founder",
    "Series A valuation",
    "Fed inflation recession",
]

feedparser.USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _extract_tweet_id(url: str) -> str | None:
    match = re.search(r"/status/(\d+)", url)
    return match.group(1) if match else None


def _working_instance() -> str | None:
    for instance in NITTER_INSTANCES:
        try:
            feed = feedparser.parse(f"{instance}/search/rss?q=VC&f=tweets")
            if getattr(feed, "status", 0) == 200 and feed.entries:
                return instance
        except Exception:
            continue
    return None


def search_tweets(max_results: int = 10) -> list[dict]:
    print("  Finding working Nitter instance...")
    instance = _working_instance()
    if not instance:
        print("  All Nitter instances down.")
        return []
    print(f"  Using {instance}")

    collected = []
    seen_ids = set()

    for query in QUERIES:
        url = f"{instance}/search/rss?q={query.replace(' ', '+')}&f=tweets"
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue
        if getattr(feed, "status", 0) >= 400:
            continue

        for entry in feed.entries:
            tweet_id = _extract_tweet_id(entry.get("link", ""))
            if not tweet_id or tweet_id in seen_ids:
                continue
            seen_ids.add(tweet_id)

            author = entry.get("author", "unknown")
            text = entry.get("title", entry.get("summary", "")).strip()
            text = re.sub(r"<[^>]+>", "", text)  # strip HTML

            collected.append({
                "id": tweet_id,
                "text": text[:280],
                "author": author if author.startswith("@") else f"@{author}",
                "likes": 0,
                "retweets": 0,
                "url": f"https://twitter.com/i/web/status/{tweet_id}",
            })

        if len(collected) >= max_results:
            break

    return collected[:max_results]
