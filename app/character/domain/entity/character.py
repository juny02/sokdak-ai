from pydantic import AwareDatetime, BaseModel
from ulid import ULID

from app.character.domain.enum.character_type import CharacterType
from app.character.domain.valueobject.persona import Persona


class Character(BaseModel):
    id: ULID
    user_id: ULID
    name: str
    persona: Persona
    type: CharacterType
    last_chat_at: AwareDatetime | None = None
    created_at: AwareDatetime
    updated_at: AwareDatetime
