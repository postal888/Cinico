# Cinico

An X/Twitter agent that drafts and posts tweets. No motivational filler, no emojis, no hashtags — just text.

## What it does

- Scans current news and cases: pitch decks, startups, macro, markets, VC theater.
- Drafts tweets in a cynical, dry voice. One thought per tweet, 280 chars max.
- Waits for the human to pick a draft before anything ships to X.

## Voice

- Opens with a hard observation or a question.
- Specifics over slogans. Numbers and mechanics when they exist.
- Opinions, not investment advice.

See `CLAUDE.md` for the full style guide the agent follows.

## Workflow

1. Pull 3–5 fresh items from the covered topics.
2. Produce 3 tweet variants per item.
3. Stop. Human picks one. Only then it gets posted.
