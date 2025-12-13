from pydantic import BaseModel
from ulid import ULID

from app.character.domain.enum import CharacterType
from app.character.domain.valueobject import Persona


class CreateCharacterCommand(BaseModel):
    user_id: ULID
    name: str
    persona: Persona
    type: CharacterType