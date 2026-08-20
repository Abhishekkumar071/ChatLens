# parsers/whatsapp.py
import re
from datetime import datetime
from models import Message


# Matches lines like: "15/01/24, 10:30 - Abhishek: Hey, how are you?"
# Breakdown of the pattern:
#   ^(\d{1,2}/\d{1,2}/\d{2,4})  -> date, e.g. 15/01/24 or 1/1/2024
#   ,\s(\d{1,2}:\d{2}(?:\s?[ap]m)?)  -> time, with optional am/pm
#   \s-\s  -> the literal " - " separator
#   ([^:]+):  -> sender name, anything up to the next colon
#   \s(.*)  -> the actual message text
MESSAGE_PATTERN = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}(?:\s?[APap][Mm])?)\s-\s([^:]+):\s(.*)$"
)

# Common timestamp formats to try, in order, since regional exports vary.
TIMESTAMP_FORMATS = [
    "%d/%m/%y %H:%M",
    "%d/%m/%Y %H:%M",
    "%m/%d/%y %H:%M",
    "%m/%d/%Y %H:%M",
    "%d/%m/%y %I:%M %p",
    "%d/%m/%Y %I:%M %p",
]


def _parse_timestamp(date_str: str, time_str: str) -> datetime:
    """
    Tries multiple date/time format combinations since WhatsApp's
    export format varies by phone region and OS.
    Raises ValueError if none match — caller decides how to handle that.
    """
    combined = f"{date_str} {time_str}"
    for fmt in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(combined, fmt)
        except ValueError:
            continue
    raise ValueError(f"Could not parse timestamp: {combined}")


def parse_whatsapp_txt(file_content: bytes) -> list[Message]:
    """
    Parses a raw WhatsApp .txt export (as bytes) into a list of
    validated Message objects. Handles multi-line messages by
    appending continuation lines to the previous message.
    """
    text = file_content.decode("utf-8", errors="ignore")
    lines = text.split("\n")

    parsed: list[Message] = []
    skipped = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = MESSAGE_PATTERN.match(line)

        if match:
            date_str, time_str, sender, msg_text = match.groups()
            try:
                timestamp = _parse_timestamp(date_str, time_str)
            except ValueError:
                skipped += 1
                continue

            try:
                parsed.append(
                    Message(
                        timestamp=timestamp,
                        sender=sender.strip(),
                        text=msg_text,
                        platform="whatsapp",
                    )
                )
            except Exception:
                skipped += 1
                continue
        else:
            # No timestamp match -> this line is a continuation of
            # the previous message (a line break within one message).
            if parsed:
                parsed[-1].text += f"\n{line}"
            else:
                skipped += 1  # stray line before any real message

    return parsed
