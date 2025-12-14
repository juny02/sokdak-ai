from pydantic import BaseModel

from app.character.domain.entity import Character
from app.character.domain.enum import CharacterType

from .persona_response import PersonaResponse


class BaseCharacterResponse(BaseModel):
    id: str
    user_id: str
    name: str
    persona: PersonaResponse
    type: CharacterType
    last_chat_at: str | None = None
    created_at: str
    updated_at: str
    
    @classmethod
    def from_domain(cls, character: Character) -> "BaseCharacterResponse":
        return cls(
            id=str(character.id),
            user_id=str(character.user_id),
            name=character.name,
            persona=PersonaResponse.from_domain(character.persona),
            type=character.type,
            last_chat_at=(
                character.last_chat_at.isoformat()
                if character.last_chat_at
                else None
            ),
            created_at=character.created_at.isoformat(),
            updated_at=character.updated_at.isoformat(),
        )
