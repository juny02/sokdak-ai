from app.chat.application.command import StartConversationCommand
from app.chat.domain.entity import Conversation
from app.chat.domain.repository import ConversationRepository


class StartConversationUseCase:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
    ):
        self.conversation_repo = conversation_repo

    async def __call__(self, cmd: StartConversationCommand) -> Conversation:
        return await self.conversation_repo.create(
            user_id=cmd.user_id,
            character_id=cmd.character_id,
            language=cmd.language,
        )
