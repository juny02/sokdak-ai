from app.chat.application.command import GetConversationsCommand
from app.chat.domain.entity import Conversation
from app.chat.domain.repository import ConversationRepository


class GetConversationsUseCase:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
    ):
        self.conversation_repo = conversation_repo

    async def __call__(self, cmd: GetConversationsCommand) -> Conversation:
        return await self.conversation_repo.get(
            order_by=cmd.order_by,
            user_id=cmd.user_id,
            character_id=cmd.character_id,
        )
