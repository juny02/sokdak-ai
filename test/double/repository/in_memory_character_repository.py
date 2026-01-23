from datetime import datetime, timezone

from ulid import ULID

from app.character.application.command import OrderBy
from app.character.domain.entity import Character
from app.character.domain.enum import Appearance, CharacterType
from app.character.domain.repository import CharacterRepository
from app.character.domain.valueobject import Persona


class InMemoryCharacterRepository(CharacterRepository):
    """
    테스트를 위한 In-Memory CharacterRepository 구현체입니다.

    - 실제 DB를 사용하지 않고 메모리 상에 Character를 저장합니다.
    - 이 구현체는 테스트 환경에서만 사용되며, 프로덕션 코드에서는 사용되지 않습니다.
    """

    def __init__(self):
        self._store: dict[ULID, Character] = {}

    async def create(
        self,
        user_id: ULID,
        name: str,
        persona: Persona,
        appearance: Appearance,
        type: CharacterType,
    ) -> Character:
        now = datetime.now(timezone.utc)

        character = Character(
            id=ULID(),
            user_id=user_id,
            name=name,
            persona=persona,
            appearance=appearance,
            type=type,
            last_chat_at=None,
            created_at=now,
            updated_at=now,
        )

        self._store[character.id] = character
        return character

    async def get(
        self,
        order_by: OrderBy,
        user_id: ULID | None = None,
        type: CharacterType | None = None,
    ) -> list[Character]:
        values = list(self._store.values())

        # filtering
        if user_id:
            values = [c for c in values if c.user_id == user_id]
        if type:
            values = [c for c in values if c.type == type]

        # ordering
        if order_by == OrderBy.ASC:
            values.sort(key=lambda c: c.created_at)
        elif order_by == OrderBy.DESC:
            values.sort(key=lambda c: c.created_at, reverse=True)
        elif order_by == OrderBy.CURR:
            values.sort(
                key=lambda c: c.last_chat_at or c.created_at,
                reverse=True,
            )

        return values

    async def get_by_id(self, id: ULID) -> Character | None:
        return self._store.get(id)

    async def update(self, character: Character) -> Character:
        self._store[character.id] = character
        return character

    async def delete_by_id(self, id: ULID) -> None:
        self._store.pop(id, None)
