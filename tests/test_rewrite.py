import json

from rewrite import no_dashes, rewrite_item


def test_no_dashes_replaces_em_dash():
    assert no_dashes("Milan Fashion Week — Day One") == "Milan Fashion Week, Day One"


def test_no_dashes_replaces_double_hyphen():
    assert no_dashes("New material -- lighter than cotton") == "New material, lighter than cotton"


class _FakeContent:
    def __init__(self, text):
        self.text = text


class _FakeMessage:
    def __init__(self, text):
        self.content = [_FakeContent(text)]


class _FakeMessages:
    def __init__(self, text):
        self._text = text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _FakeMessage(self._text)


class _FakeClient:
    def __init__(self, text):
        self.messages = _FakeMessages(text)


def test_rewrite_item_parses_json_response_and_strips_dashes():
    fake_text = json.dumps({
        "headline": "Lab-Grown Leather Enters Production — At Scale",
        "blurb": "Design teams gain a durable, low-impact material option.",
    })
    client = _FakeClient(fake_text)

    result = rewrite_item(client, "WWD", "orig title", "orig summary")

    assert result["headline"] == "Lab-Grown Leather Enters Production, At Scale"
    assert result["blurb"] == "Design teams gain a durable, low-impact material option."
    assert client.messages.calls[0]["model"] == "claude-haiku-4-5-20251001"
