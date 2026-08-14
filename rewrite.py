import json
import re

_DASH = re.compile(r"\s*[—–―]\s*|\s+-{2,}\s+")


def no_dashes(text: str) -> str:
    if not text:
        return text
    t = _DASH.sub(", ", text)
    t = re.sub(r"\s+,", ",", t)
    t = re.sub(r",\s*,+", ", ", t)
    t = re.sub(r",\s*([.;:!?])", r"\1", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t


REWRITE_MODEL = "claude-haiku-4-5-20251001"

_PROMPT = """You are writing a one-line entry for a scrolling news ticker on a B2B fashion trade publication read by design teams and buyers.

Source: {source}
Original headline: {title}
Original summary: {summary}

Write, in your own words (do not copy phrases from the original):
1. A rewritten headline, under 90 characters.
2. One sentence (under 140 characters) on why this matters for a design or product team.

Respond with ONLY valid JSON, no other text: {{"headline": "...", "blurb": "..."}}"""


def rewrite_item(client, source: str, title: str, summary: str) -> dict:
    message = client.messages.create(
        model=REWRITE_MODEL,
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": _PROMPT.format(source=source, title=title, summary=summary),
        }],
    )
    data = json.loads(message.content[0].text)
    return {
        "headline": no_dashes(data["headline"]).strip(),
        "blurb": no_dashes(data["blurb"]).strip(),
    }
