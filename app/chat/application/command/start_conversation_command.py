from pydantic import BaseModel
from ulid import ULID

from app.chat.domain.enum import ConversationType, Language


class StartConversationCommand(BaseModel):
    character_id: ULID
    user_id: ULID
    language: Language
    conversation_type: ConversationType
