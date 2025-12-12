from app.chat.application.command import GetMessagesCommand
from app.chat.domain.entity import Message
from app.chat.domain.repository import MessageRepository


class GetMessagesUseCase:
    """
    특정 대화의 모든 메세지들을 가져옵니다.
    """

    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    async def __call__(self, cmd: GetMessagesCommand) -> list[Message]:
        return await self.message_repo.get(
            conversation_id=cmd.conversation_id,
            limit=cmd.limit,
            before=cmd.before,
        )
