from app.chat.application.command import UpdateConversationCommand
from app.chat.domain.entity import Conversation
from app.chat.domain.repository import ConversationRepository


class UpdateConversationUseCase:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
    ):
        self.conversation_repo = conversation_repo

    async def __call__(self, cmd: UpdateConversationCommand) -> Conversation:
        # 기존 대화 조회
        conversation = await self.conversation_repo.get_by_id(id=cmd.id)
        # 대회 업데이트
        if cmd.summary is not None:
            conversation.update_summary(cmd.summary)
        if cmd.last_message is not None:
            conversation.update_last_message(cmd.last_message)
        # 변경된 대화 저장
        await self.conversation_repo.update(conversation=conversation)
