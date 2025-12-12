from ulid import ULID

from app.chat.domain.entity import Conversation
from app.chat.domain.repository import ConversationRepository


class GetConversationUseCase:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
    ):
        self.conversation_repo = conversation_repo

    async def __call__(self, conversation_id: ULID) -> Conversation:
        return await self.conversation_repo.get_by_id(id=conversation_id)
