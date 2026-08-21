from pathlib import Path
from parsers.telegram import parse_telegram_json

FIXTURE = Path(__file__).parent / "fixtures" / "sample_telegram.json"


def test_skips_service_messages():
    content = FIXTURE.read_bytes()
    messages = parse_telegram_json(content)
    # 3 entries in the file, but 1 is a "service" type -> only 2 real messages
    assert len(messages) == 2


def test_flattens_rich_text():
    content = FIXTURE.read_bytes()
    messages = parse_telegram_json(content)
    priya_msg = messages[1]
    assert priya_msg.text == "Check this out"