from datetime import datetime

from beanie import Document
from pydantic import Field
from ulid import ULID

from app.chat.domain.enum.role import Role


class MessageDocument(Document):
    """
    MongoDB에 저장되는 Message Persistence Model
    """

    id: ULID = Field(default_factory=ULID, alias="_id")
    conversation_id: ULID
    role: Role
    content: str
    created_at: datetime

    # TODO: index 추가
    class Settings:
        name = "messages"
        bson_encoders = {ULID: str}
