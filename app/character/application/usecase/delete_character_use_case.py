from ulid import ULID

from app.character.domain.repository import CharacterRepository
from app.chat.application.command import OrderBy
from app.chat.domain.repository import ConversationRepository, MessageRepository


class DeleteCharacterUseCase:
    """
    캐릭터를 삭제합니다.

    흐름:
        1) 캐릭터가 보유한 대화 조회 (캐릭터 1개 당 대화 1개)
        2) 대화의 메시지 삭제
        3) 대화 삭제
        4) 캐릭터 삭제
    """

    def __init__(
        self,
        character_repo: CharacterRepository,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository,
    ):
        self.character_repo = character_repo
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo

    async def __call__(self, character_id: ULID) -> None:
        # 1) 캐릭터가 보유한 대화 조회
        conversation_list = await self.conversation_repo.get(
            order_by=OrderBy.DESC, character_id=character_id
        )

        for conversation in conversation_list:
            # 2) 대화의 메시지 삭제
            await self.message_repo.delete_by_conversation_id(
                conversation_id=conversation.id
            )
            # 3) 대화 삭제
            await self.conversation_repo.delete(id=conversation.id)

        # 4) 캐릭터 삭제
        await self.character_repo.delete_by_id(id=character_id)
