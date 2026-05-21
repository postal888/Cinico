#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from searcher import search_tweets
from fetcher import fetch_tweet
from drafter import draft_replies
from poster import post_reply

load_dotenv()


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set in .env")
        return

    print("Searching Twitter...")
    tweets = search_tweets(max_results=10)

    if not tweets:
        print("\nSearch failed. Paste a tweet URL manually instead.")
        url = input("Tweet URL or ID: ").strip()
        if not url:
            return
        try:
            tweets = [fetch_tweet(url)]
        except Exception as e:
            print(f"Error: {e}")
            return

    print(f"\nFound {len(tweets)} tweets:\n")
    for i, t in enumerate(tweets, 1):
        preview = t["text"][:80].replace("\n", " ")
        print(f"[{i}] {t['author']}")
        print(f"    {preview}")
        print()

    print("[q] quit")
    choice = input("Choose tweet: ").strip().lower()
    if choice == "q" or not choice:
        return
    try:
        tweet = tweets[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    print(f'\n"{tweet["text"]}"')
    print("\nDrafting replies...")
    try:
        drafts = draft_replies(tweet)
    except Exception as e:
        print(f"Draft error: {e}")
        return

    if not drafts:
        print("No drafts generated.")
        return

    print()
    for i, d in enumerate(drafts, 1):
        print(f"[{i}] {d}\n")

    print("[s] skip  [q] quit")
    choice = input("Choose reply: ").strip().lower()
    if choice in ("q", "s", ""):
        print("Aborted.")
        return
    try:
        chosen = drafts[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    confirm = input(f'\nPost this?\n"{chosen}"\n[y/n]: ').strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    print("Posting...")
    try:
        url_out = post_reply(chosen, tweet["id"])
        print(f"Posted: {url_out}")
    except Exception as e:
        print(f"Post error: {e}")


if __name__ == "__main__":
    main()
