from dataclasses import dataclass
from datetime import datetime, timezone

from ulid import ULID

from app.character.domain.enum.character_type import CharacterType
from app.character.domain.valueobject.persona import Persona


@dataclass
class Character:
    id: ULID
    user_id: ULID
    name: str
    persona: Persona
    type: CharacterType
    last_chat_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    def update_name(self, name: str) -> None:
        self.name = name
        self.updated_at = datetime.now(timezone.utc)

    def update_persona(self, persona: Persona) -> None:
        self.persona = persona
        self.updated_at = datetime.now(timezone.utc)
