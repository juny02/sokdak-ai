from abc import ABC, abstractmethod

from ulid import ULID

from app.character.application.command import OrderBy
from app.character.domain.entity import Character
from app.character.domain.enum import Appearance, CharacterType
from app.character.domain.valueobject import Persona


class CharacterRepository(ABC):
    @abstractmethod
    async def get(
        self,
        user_id: ULID | None,
        order_by: OrderBy,
        type: CharacterType | None,
    ) -> list[Character]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: ULID) -> Character | None:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        user_id: ULID,
        name: str,
        persona: Persona,
        appearance: Appearance,
        type: CharacterType,
    ) -> Character:
        raise NotImplementedError

    @abstractmethod
    async def update(self, character: Character) -> Character:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, id: ULID) -> None:
        raise NotImplementedError
