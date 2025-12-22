from datetime import datetime, timezone

from ulid import ULID

from app.chat.application.command import OrderBy
from app.chat.domain.entity import Conversation
from app.chat.domain.enum import ConversationType, Language
from app.chat.domain.repository import ConversationRepository


class InMemoryConversationRepository(ConversationRepository):
    """
    테스트를 위한 In-Memory ConversationRepository 구현체입니다.

    - 실제 DB를 사용하지 않고 메모리 상에 Conversation을 저장합니다.
    - 이 구현체는 테스트 환경에서만 사용되며, 프로덕션 코드에서는 사용되지 않습니다.
    """

    def __init__(self):
        self._store: dict[ULID, Conversation] = {}

    async def create(
        self,
        character_id: ULID,
        user_id: ULID,
        language: Language,
        conversation_type: ConversationType,
    ) -> Conversation:
        conv = Conversation(
            id=ULID(),
            character_id=character_id,
            user_id=user_id,
            summary=None,
            last_message=None,
            last_message_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            language=language,
            conversation_type=conversation_type,
        )
        self._store[conv.id] = conv
        return conv

    async def get(
        self,
        order_by: OrderBy,
        user_id: ULID | None = None,
        character_id: ULID | None = None,
    ) -> list[Conversation]:
        values = list(self._store.values())

        if user_id:
            values = [c for c in values if c.user_id == user_id]
        if character_id:
            values = [c for c in values if c.character_id == character_id]

        if order_by == OrderBy.ASC:
            values.sort(key=lambda c: c.created_at)

        elif order_by == OrderBy.DESC:
            values.sort(key=lambda c: c.created_at, reverse=True)

        elif order_by == OrderBy.CURR:
            # last_message_at이 None인 건 맨 뒤로
            values.sort(
                key=lambda c: c.last_message_at or c.created_at,
                reverse=True,
            )

        return values

    async def get_by_id(self, id: ULID) -> Conversation | None:
        return self._store.get(id)

    async def update(self, conversation: Conversation) -> Conversation:
        self._store[conversation.id] = conversation
        return conversation

    async def delete(self, id: ULID) -> None:
        self._store.pop(id, None)
