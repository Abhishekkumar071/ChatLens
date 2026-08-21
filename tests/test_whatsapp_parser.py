from pathlib import Path
from parsers.whatsapp import parse_whatsapp_txt

FIXTURE = Path(__file__).parent / "fixtures" / "sample_whatsapp.txt"


def test_parses_correct_message_count():
    content = FIXTURE.read_bytes()
    messages = parse_whatsapp_txt(content)
    # 3 real messages (the continuation line merges into message 2, not a 4th)
    assert len(messages) == 3


def test_multiline_message_is_merged():
    content = FIXTURE.read_bytes()
    messages = parse_whatsapp_txt(content)
    priya_msg = messages[1]
    assert priya_msg.sender == "Priya"
    assert "continuation line" in priya_msg.text


def test_sender_and_text_extracted_correctly():
    content = FIXTURE.read_bytes()
    messages = parse_whatsapp_txt(content)
    assert messages[0].sender == "Abhishek"
    assert messages[0].text == "Hey, how are you?"


def test_media_message_detected():
    content = FIXTURE.read_bytes()
    messages = parse_whatsapp_txt(content)
    assert messages[2].text.strip() == "<Media omitted>"