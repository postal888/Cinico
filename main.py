#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from fetcher import fetch_news
from drafter import draft_tweets
from poster import post_tweet

load_dotenv()


def pick(options: list[str], prompt: str) -> str | None:
    for i, opt in enumerate(options, 1):
        print(f"\n[{i}] {opt}")
    print("\n[s] skip  [q] quit")
    choice = input(f"\n{prompt}: ").strip().lower()
    if choice == "q":
        return "quit"
    if choice == "s":
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except ValueError:
        pass
    return None


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set in .env")
        return

    print("Fetching news...")
    items = fetch_news(max_items=5)
    if not items:
        print("No news fetched. Check feed URLs.")
        return

    titles = [item["title"] for item in items]
    print(f"\nFound {len(items)} items. Pick one to draft tweets for:")
    chosen_title = pick(titles, "Choose item")
    if chosen_title == "quit":
        return
    if chosen_title is None:
        print("Nothing selected.")
        return

    item = next(i for i in items if i["title"] == chosen_title)

    print("\nDrafting tweets...")
    drafts = draft_tweets(item)
    if not drafts:
        print("Draft generation failed.")
        return

    print("\nPick a tweet to post:")
    chosen_tweet = pick(drafts, "Choose tweet")
    if chosen_tweet == "quit":
        return
    if chosen_tweet is None:
        print("Nothing posted.")
        return

    confirm = input(f'\nPost this?\n"{chosen_tweet}"\n[y/n]: ').strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    print("Posting...")
    url = post_tweet(chosen_tweet)
    print(f"Posted: {url}")


if __name__ == "__main__":
    main()
