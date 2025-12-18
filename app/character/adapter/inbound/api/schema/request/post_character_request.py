from pydantic import BaseModel, ConfigDict
from ulid import ULID

from app.character.domain.enum import CharacterType

from .persona_request import PersonaRequest


class PostCharacterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: ULID
    name: str
    persona: PersonaRequest
    type: CharacterType
