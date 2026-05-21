import anthropic
import os

SYSTEM_PROMPT = """You write tweets in English. Tone: cynical, dry, zero motivational filler.
Max 280 characters. One thought, one tweet. No emojis, no hashtags, text only.

Topics: pitch decks and startups from an investor's POV, macro/markets (reality vs press releases), VC/founder bullshit.

Style rules:
- Open with a hard observation or a question
- Specifics over slogans. Numbers and mechanics when available
- Opinions only, never investment advice
- Never name-drop the source article or say "according to"

Return exactly 3 tweet variants, numbered 1. 2. 3. — nothing else."""


def draft_tweets(news_item: dict) -> list[str]:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"Title: {news_item['title']}\nContext: {news_item['summary']}"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    tweets = []
    for line in raw.split("\n"):
        line = line.strip()
        if line and line[0].isdigit() and line[1] in ".":
            tweets.append(line[2:].strip() if len(line) > 2 else "")
        elif line and not tweets and not line[0].isdigit():
            tweets.append(line)

    return [t for t in tweets if t][:3]
