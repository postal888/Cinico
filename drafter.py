import anthropic
import os

SYSTEM_PROMPT = """You write replies to tweets. English only. Tone: cynical, dry, zero motivational filler.
Max 280 characters. One thought, one reply. No emojis, no hashtags, text only.

Topics you engage with: pitch decks, startups, VC theater, macro/markets, founder bullshit.

Style rules:
- Open with a hard observation or a sharp question
- Specifics over slogans. Numbers and mechanics when available
- Opinions only, never investment advice
- The reply must be self-contained — readable without seeing the original tweet
- Never start with "I", never say "great point", never be agreeable for the sake of it

Return exactly 3 reply variants, numbered 1. 2. 3. — nothing else."""


def draft_replies(tweet: dict) -> list[str]:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = (
        f"Tweet by {tweet['author']}:\n"
        f'"{tweet["text"]}"\n\n'
        f"Likes: {tweet['likes']}  Retweets: {tweet['retweets']}"
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    replies = []
    for line in raw.split("\n"):
        line = line.strip()
        if line and len(line) > 2 and line[0].isdigit() and line[1] in ".)":
            replies.append(line[2:].strip())

    return [r for r in replies if r][:3]
