#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from searcher import search_tweets
from drafter import draft_replies
from poster import post_reply

load_dotenv()


def pick_index(count: int, prompt: str) -> int | None:
    print(f"\n[s] skip  [q] quit")
    choice = input(f"{prompt}: ").strip().lower()
    if choice == "q":
        raise SystemExit
    if choice == "s":
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < count:
            return idx
    except ValueError:
        pass
    print("Invalid choice, skipping.")
    return None


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set in .env")
        return

    print("Searching Twitter...")
    tweets = search_tweets(max_results=10)
    if not tweets:
        print("No tweets found.")
        return

    print(f"\nFound {len(tweets)} tweets. Pick one to reply to:\n")
    for i, t in enumerate(tweets, 1):
        metrics = f"♥{t['likes']} RT{t['retweets']}"
        preview = t["text"][:80].replace("\n", " ")
        print(f"[{i}] {t['author']}  {metrics}")
        print(f"    {preview}")
        print()

    idx = pick_index(len(tweets), "Choose tweet")
    if idx is None:
        return

    tweet = tweets[idx]
    print(f"\nSelected: {tweet['url']}")
    print(f'"{tweet["text"][:200]}"')

    print("\nDrafting replies...")
    drafts = draft_replies(tweet)
    if not drafts:
        print("Draft generation failed.")
        return

    print("\nPick a reply:\n")
    for i, d in enumerate(drafts, 1):
        print(f"[{i}] {d}")
        print()

    idx = pick_index(len(drafts), "Choose reply")
    if idx is None:
        return

    chosen = drafts[idx]
    confirm = input(f'\nPost this reply?\n"{chosen}"\n[y/n]: ').strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    print("Posting...")
    url = post_reply(chosen, tweet["id"])
    print(f"Posted: {url}")


if __name__ == "__main__":
    main()
