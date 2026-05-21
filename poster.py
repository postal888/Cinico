import tweepy
import os


def get_client() -> tweepy.Client:
    return tweepy.Client(
        bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )


def post_reply(text: str, in_reply_to_tweet_id: str) -> str:
    client = get_client()
    response = client.create_tweet(
        text=text,
        in_reply_to_tweet_id=in_reply_to_tweet_id,
    )
    tweet_id = response.data["id"]
    return f"https://twitter.com/i/web/status/{tweet_id}"
