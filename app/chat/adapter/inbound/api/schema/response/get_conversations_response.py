from pydantic import BaseModel

from app.chat.domain.entity import Conversation

from .base_conversation_response import BaseConversationResponse


class GetConversationsResponse(BaseModel):
    items: list[BaseConversationResponse]

    @classmethod
    def from_domain(cls, conversations: list[Conversation]):
        return cls(
            items=[BaseConversationResponse.from_domain(c) for c in conversations],
        )
