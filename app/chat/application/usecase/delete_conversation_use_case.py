from ulid import ULID

from app.chat.domain.repository import ConversationRepository, MessageRepository


class DeleteConversationUseCase:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository,
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo

    async def __call__(self, conversation_id: ULID) -> None:
        await self.message_repo.delete_by_conversation_id(
            conversation_id=conversation_id
        )
        await self.conversation_repo.delete(id=conversation_id)
