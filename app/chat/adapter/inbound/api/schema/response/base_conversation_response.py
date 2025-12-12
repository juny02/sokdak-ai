from pydantic import BaseModel

from app.chat.domain.entity import Conversation


class BaseConversationResponse(BaseModel):
    id: str
    character_id: str
    summary: str | None = None
    last_message: str | None = None
    last_message_at: str | None = None
    created_at: str
    updated_at: str

    @classmethod
    def from_domain(cls, conversation: Conversation) -> "BaseConversationResponse":
        return cls(
            id=str(conversation.id),
            character_id=str(conversation.character_id),
            summary=conversation.summary,
            last_message=conversation.last_message,
            last_message_at=(
                conversation.last_message_at.isoformat()
                if conversation.last_message_at
                else None
            ),
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat(),
        )
