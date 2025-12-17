from abc import ABC, abstractmethod

from ulid import ULID

from app.chat.application.command import OrderBy
from app.chat.domain.entity.conversation import Conversation
from app.chat.domain.enum import Language


class ConversationRepository(ABC):
    @abstractmethod
    async def create(
        self, character_id: ULID, user_id: ULID, language: Language
    ) -> Conversation:
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

    @abstractmethod
    async def get_by_character_id(self, character_id: ULID) -> Conversation | None:
        raise NotImplementedError
