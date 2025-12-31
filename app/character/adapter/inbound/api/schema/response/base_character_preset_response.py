from pydantic import BaseModel

from app.character.domain.valueobject.character_preset import CharacterPreset

from ..response.persona_response import PersonaResponse


class BaseCharacterPresetResponse(BaseModel):
    key: str
    name: str
    description: str
    persona: PersonaResponse

    @classmethod
    def from_domain(cls, preset: CharacterPreset) -> "BaseCharacterPresetResponse":
        return cls(
            key=preset.key,
            name=preset.name,
            description=preset.description,
            persona=PersonaResponse.from_domain(preset.persona),
        )
