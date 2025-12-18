from datetime import datetime

from beanie import Document
from pydantic import Field
from ulid import ULID

from app.chat.domain.enum import ConversationType, Language


class ConversationDocument(Document):
    """
    MongoDB에 저장되는 Conversation Document Model
    """

    id: ULID = Field(default_factory=ULID, alias="_id")
    user_id: ULID
    character_id: ULID
    summary: str | None
    last_message: str | None
    last_message_at: datetime | None
    created_at: datetime
    updated_at: datetime
    language: Language
    conversation_type: ConversationType

    # TODO: index 추가
    class Settings:
        name = "conversations"
        bson_encoders = {ULID: str}
