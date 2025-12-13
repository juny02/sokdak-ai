from abc import ABC, abstractmethod

from ulid import ULID

from app.character.application.command.order_by import OrderBy
from app.character.domain.entity.character import Character
from app.character.domain.enum.character_type import CharacterType


class CharacterRepository(ABC):
    @abstractmethod
    async def get(
        self,
        order_by: OrderBy,
        user_id: ULID | None = None,
        type: CharacterType | None = None,
    ) -> list[Character]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: ULID) -> Character | None:
        raise NotImplementedError
