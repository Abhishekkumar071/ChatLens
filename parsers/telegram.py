# parsers/telegram.py
import json
from typing import Union
from models import Message


def _flatten_text(raw_text: Union[str, list]) -> str:
    """
    Telegram's 'text' field is either a plain string, or a list of
    mixed strings and rich-text objects (for bold/links/mentions/etc).
    This normalizes both cases into a single plain string.
    """
    if isinstance(raw_text, str):
        return raw_text

    if isinstance(raw_text, list):
        parts = []
        for chunk in raw_text:
            if isinstance(chunk, str):
                parts.append(chunk)
            elif isinstance(chunk, dict):
                # rich-text object, e.g. {"type": "bold", "text": "this"}
                parts.append(chunk.get("text", ""))
        return "".join(parts)

    return ""


# parsers/telegram.py — parse_telegram_json() ke start mein add karo

def parse_telegram_json(file_content: bytes) -> list[Message]:
    """
    Parses a raw Telegram JSON export (as bytes, e.g. from a Streamlit
    file uploader) into a list of validated Message objects.

    Skips 'service' entries (pins, member changes, etc.) since those
    aren't real conversational messages.
    """
    data = json.loads(file_content)

    if not isinstance(data, dict):
        raise ValueError("Invalid Telegram export format — expected a JSON object at the root.")

    raw_messages = data.get("messages", [])
    if not isinstance(raw_messages, list):
        raise ValueError("Invalid Telegram export format — 'messages' field is missing or malformed.")

    # ... baaki function same rahega
    raw_messages = data.get("messages", [])

    parsed: list[Message] = []
    skipped = 0

    for entry in raw_messages:
        if entry.get("type") != "message":
            skipped += 1
            continue

        sender = entry.get("from")
        timestamp = entry.get("date")
        text = _flatten_text(entry.get("text", ""))

        if not sender or not timestamp:
            # Malformed entry — missing required fields.
            # We skip rather than crash the whole import.
            skipped += 1
            continue

        try:
            parsed.append(
                Message(
                    timestamp=timestamp,
                    sender=sender,
                    text=text,
                    platform="telegram",
                )
            )
        except Exception:
            # A single bad entry shouldn't kill the whole import —
            # we log/skip and keep going. (We'll wire real logging
            # in Step 16 - Error Handling.)
            skipped += 1
            continue

    return parsed