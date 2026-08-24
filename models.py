# models.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class Message(BaseModel):
    model_config = {"frozen": True}  # ye line — makes it hashable
    """
    Canonical representation of a single chat message,
    regardless of which platform it originated from.
    """

    timestamp: datetime
    sender: str
    text: str
    platform: str  # "telegram" or "whatsapp"

    @field_validator("sender")
    @classmethod
    def sender_must_not_be_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("sender cannot be blank")
        return v

    @field_validator("text")
    @classmethod
    def text_default_empty(cls, v: Optional[str]) -> str:
        # A message can legitimately be empty (e.g. a media-only message
        # with the caption stripped) — we normalize None -> "" here
        # rather than letting None leak into downstream string operations.
        return v or ""