from datetime import datetime, timezone
from typing import List

from ulid import ULID

from app.chat.domain.entity import Message
from app.chat.domain.enum import Role
from app.chat.domain.repository import MessageRepository


class InMemoryEphemeralMessageRepository(MessageRepository):
    """
    테스트를 위한 In-Memory Ephemeral MessageRepository 구현체입니다.

    - 실제 Redis를 사용하지 않고 메모리 상에 Message를 저장합니다.
    - 이 구현체는 테스트 환경에서만 사용되며, 프로덕션 코드에서는 사용되지 않습니다.
    """

    def __init__(self):
        self._is_called = False  # 어떤 레포지토리가 호출되었는지 확인하기 위한 플래그
        self._store: dict[ULID, List[Message]] = {}

    async def create(
        self,
        conversation_id: ULID,
        role: Role,
        content: str,
    ) -> Message:
        self._is_called = True

        message = Message(
            id=ULID(),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc),
        )

        self._store.setdefault(conversation_id, []).append(message)
        return message

    async def get(
        self,
        conversation_id: ULID,
        limit: int,
        before: ULID | None,
    ) -> list[Message]:
        self._is_called = True

        messages = self._store.get(conversation_id, [])
        messages = sorted(messages, key=lambda m: m.created_at, reverse=True)

        if before:
            messages = [
                m
                for m in messages
                if m.created_at < self._get_created_at(before, conversation_id)
            ]

        return messages[:limit]

    async def delete_by_conversation_id(self, conversation_id: ULID) -> None:
        self._is_called = True

        self._store.pop(conversation_id, None)

    def _get_created_at(self, message_id: ULID, conversation_id: ULID):
        self._is_called = True

        for m in self._store.get(conversation_id, []):
            if m.id == message_id:
                return m.created_at
        return datetime.max.replace(tzinfo=timezone.utc)
