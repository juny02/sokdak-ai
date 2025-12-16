from datetime import datetime, timezone

from ulid import ULID

from app.character.application.command import OrderBy
from app.character.domain.entity import Character
from app.character.domain.enum import CharacterType, Gender, Purpose, Style, Tone
from app.character.domain.repository import CharacterRepository
from app.character.domain.valueobject import Persona


class FakeCharacterRepository(CharacterRepository):  # domain 레포지토리 상속
    async def get(
        self,
        order_by=OrderBy,
        user_id: ULID | None = None,
        type: CharacterType | None = None,
    ) -> list[Character]:
        return [
            Character(
                id=ULID(),
                user_id=user_id or ULID(),
                name="Fake Character",
                persona=Persona(
                    gender=Gender.FEMALE,
                    tone=Tone.CALM,
                    style=Style.LISTENER,
                    purpose=Purpose.CONFESSION,
                ),
                type=type or CharacterType.PERSISTENT,
                last_chat_at=None,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
            Character(
                id=ULID(),
                user_id=user_id or ULID(),
                name="Fake Character2",
                persona=Persona(
                    gender=Gender.MALE,
                    tone=Tone.CHEERFUL,
                    style=Style.ADVISOR,
                    purpose=Purpose.COUNSELING,
                ),
                type=type or CharacterType.EPHEMERAL,
                last_chat_at=None,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            ),
        ]

    async def get_by_id(self, id: ULID) -> Character | None:
        return Character(
            id=id,
            user_id=ULID(),
            name="Fake Character by ID",
            persona=Persona(
                gender=Gender.FEMALE,
                tone=Tone.CALM,
                style=Style.LISTENER,
                purpose=Purpose.CONFESSION,
            ),
            type=CharacterType.PERSISTENT,
            last_chat_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    async def create(
        self, user_id: ULID, name: str, persona: Persona, type: CharacterType
    ) -> Character:
        return Character(
            id=ULID(),
            user_id=user_id,
            name=name,
            persona=persona,
            type=type,
            last_chat_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    async def update(self, character: Character) -> Character:
        return Character

    async def delete_by_id(self, id: ULID) -> None:
        return None
