from datetime import datetime
from typing import Any, Dict, Optional

from beanie import Document
from pydantic import Field
from ulid import ULID

from app.character.domain.enum import CharacterType


class CharacterDocument(Document):
    """
    MongoDB에 저장되는 Character Document Model
    """

    id: ULID = Field(default_factory=ULID, alias="_id")
    user_id: ULID
    name: str
    type: CharacterType
    persona: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    last_chat_at: Optional[datetime] | None

    class Settings:
        name = "characters"
        indexes = [
            "user_id",
        ]
        bson_encoders = {ULID: str}
