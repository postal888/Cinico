import tweepy
import os
import re


def get_client() -> tweepy.Client:
    return tweepy.Client(
        bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        wait_on_rate_limit=True,
    )


def extract_tweet_id(url_or_id: str) -> str:
    match = re.search(r"status/(\d+)", url_or_id)
    if match:
        return match.group(1)
    if url_or_id.strip().isdigit():
        return url_or_id.strip()
    raise ValueError(f"Can't parse tweet ID from: {url_or_id}")


def fetch_tweet(url_or_id: str) -> dict:
    tweet_id = extract_tweet_id(url_or_id)
    client = get_client()
    resp = client.get_tweet(
        tweet_id,
        tweet_fields=["author_id", "text", "public_metrics"],
        expansions=["author_id"],
        user_fields=["username"],
    )
    if not resp.data:
        raise ValueError("Tweet not found")

    tweet = resp.data
    metrics = tweet.public_metrics or {}
    username = "unknown"
    if resp.includes and "users" in resp.includes:
        username = f"@{resp.includes['users'][0].username}"

    return {
        "id": str(tweet.id),
        "text": tweet.text,
        "author": username,
        "likes": metrics.get("like_count", 0),
        "retweets": metrics.get("retweet_count", 0),
        "url": f"https://twitter.com/i/web/status/{tweet.id}",
    }
