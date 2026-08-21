from parsers.whatsapp import parse_whatsapp_txt
from processing.enrich import messages_to_dataframe
from pathlib import Path

FIXTURE = Path(__file__).parent / "fixtures" / "sample_whatsapp.txt"


def test_media_message_has_zero_word_count():
    messages = parse_whatsapp_txt(FIXTURE.read_bytes())
    df = messages_to_dataframe(messages)
    media_row = df[df["is_media"]].iloc[0]
    assert media_row["word_count"] == 0


def test_empty_message_list_returns_empty_dataframe():
    df = messages_to_dataframe([])
    assert len(df) == 0
    assert "word_count" in df.columns  # correct shape even when empty