import tweepy
import os

QUERIES = [
    "startup funding round -is:retweet lang:en",
    "pitch deck investors -is:retweet lang:en",
    "venture capital founder -is:retweet lang:en",
    "Series A Series B valuation -is:retweet lang:en",
    "Fed inflation recession -is:retweet lang:en",
    "unicorn IPO -is:retweet lang:en",
]

TWEET_FIELDS = ["author_id", "text", "public_metrics", "created_at"]
EXPANSIONS = ["author_id"]
USER_FIELDS = ["username", "name"]


def get_client() -> tweepy.Client:
    return tweepy.Client(
        bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        wait_on_rate_limit=True,
    )


def search_tweets(max_results: int = 10) -> list[dict]:
    client = get_client()
    collected = []
    seen_ids = set()

    for query in QUERIES:
        try:
            resp = client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=TWEET_FIELDS,
                expansions=EXPANSIONS,
                user_fields=USER_FIELDS,
            )
        except tweepy.TweepyException as e:
            print(f"  Search error: {e}")
            continue

        if not resp.data:
            continue

        users = {}
        if resp.includes and "users" in resp.includes:
            for u in resp.includes["users"]:
                users[u.id] = u

        for tweet in resp.data:
            if tweet.id in seen_ids:
                continue
            seen_ids.add(tweet.id)

            metrics = tweet.public_metrics or {}
            user = users.get(tweet.author_id)
            collected.append({
                "id": str(tweet.id),
                "text": tweet.text,
                "author": f"@{user.username}" if user else "unknown",
                "likes": metrics.get("like_count", 0),
                "replies": metrics.get("reply_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "url": f"https://twitter.com/i/web/status/{tweet.id}",
            })

        if len(collected) >= max_results * 2:
            break

    # sort by engagement
    collected.sort(key=lambda t: t["likes"] + t["retweets"] * 2, reverse=True)
    return collected[:max_results]
