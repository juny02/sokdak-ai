from abc import ABC, abstractmethod

from ulid import ULID

from app.chat.application.command import OrderBy
from app.chat.domain.entity.conversation import Conversation


class ConversationRepository(ABC):
    @abstractmethod
    async def create(self, character_id: ULID, user_id: ULID) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        order_by: OrderBy,
        user_id: ULID | None = None,
        character_id: ULID | None = None,
    ) -> list[Conversation]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: ULID) -> Conversation | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: ULID) -> None:
        raise NotImplementedError
