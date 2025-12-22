from pydantic import BaseModel

from app.chat.domain.entity import Conversation
from app.chat.domain.enum import ConversationType, Language


class BaseConversationResponse(BaseModel):
    id: str
    user_id: str
    character_id: str
    summary: str | None = None
    last_message: str | None = None
    last_message_at: str | None = None
    created_at: str
    updated_at: str
    language: Language
    conversation_type: ConversationType

    @classmethod
    def from_domain(cls, conversation: Conversation) -> "BaseConversationResponse":
        return cls(
            id=str(conversation.id),
            character_id=str(conversation.character_id),
            user_id=str(conversation.user_id),
            summary=conversation.summary,
            last_message=conversation.last_message,
            last_message_at=(
                conversation.last_message_at.isoformat()
                if conversation.last_message_at
                else None
            ),
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat(),
            language=conversation.language,
            conversation_type=conversation.conversation_type,
        )
