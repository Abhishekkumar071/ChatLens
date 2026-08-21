# processing/enrich.py
import pandas as pd
import emoji
from models import Message


MEDIA_PLACEHOLDER = "<Media omitted>"


def messages_to_dataframe(messages: list[Message]) -> pd.DataFrame:
    """
    Converts a list of validated Message objects into a single
    enriched DataFrame that the rest of the app builds on.
    """
    if not messages:
        return pd.DataFrame(
            columns=[
                "timestamp", "sender", "text", "platform",
                "date", "hour", "day_name", "word_count",
                "char_count", "is_media", "emojis",
            ]
        )

    df = pd.DataFrame([m.model_dump() for m in messages])

    # --- Time-based features ---
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    df["day_name"] = df["timestamp"].dt.day_name()

    # --- Media detection (before word/char counts, so media
    #     placeholders don't get counted as "content") ---
    df["is_media"] = df["text"].str.strip() == MEDIA_PLACEHOLDER

    # --- Text-based features ---
    # Media messages contribute 0 words/chars, not the length of the
    # placeholder string itself.
    df["word_count"] = df["text"].where(~df["is_media"], "").str.split().str.len().fillna(0).astype(int)
    df["char_count"] = df["text"].where(~df["is_media"], "").str.len().fillna(0).astype(int)

    # --- Emoji extraction ---
    df["emojis"] = df["text"].apply(lambda t: [c["emoji"] for c in emoji.emoji_list(t)])

    return df.sort_values("timestamp").reset_index(drop=True)