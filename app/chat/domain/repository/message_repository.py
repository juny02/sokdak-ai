from abc import ABC, abstractmethod

from ulid import ULID

from app.chat.domain.entity import Message
from app.chat.domain.enum import Role


class MessageRepository(ABC):
    @abstractmethod
    async def create(self, conversation_id: ULID, role: Role, content: str) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self, conversation_id: ULID, limit: int, before: ULID | None
    ) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_conversation_id(self, conversation_id: ULID) -> None:
        raise NotImplementedError
