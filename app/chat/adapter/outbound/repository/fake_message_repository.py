from datetime import datetime, timezone

from ulid import ULID

from app.chat.domain.entity import Message
from app.chat.domain.enum import Role
from app.chat.domain.repository import MessageRepository


class FakeMessageRepository(MessageRepository):
    async def create(self, conversation_id: ULID, role: Role, content: str) -> Message:
        return Message(
            id=ULID(),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc),
        )

    async def get(
        self, conversation_id: ULID, limit: int, before: ULID | None
    ) -> list[Message]:
        return [
            Message(
                id=ULID(),
                conversation_id=conversation_id,
                role=Role.USER,
                content="This is a placeholder message.",
                created_at=datetime.now(timezone.utc),
            )
        ]

    async def delete_by_conversation_id(self, conversation_id: ULID) -> None:
        return None
