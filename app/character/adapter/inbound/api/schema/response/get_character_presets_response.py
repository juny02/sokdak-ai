from pydantic import BaseModel

from app.character.domain.valueobject import CharacterPreset

from .base_character_preset_response import BaseCharacterPresetResponse


class GetCharacterPresetsResponse(BaseModel):
    items: list[BaseCharacterPresetResponse]

    @classmethod
    def from_domain(
        cls, character_presets: list[CharacterPreset]
    ) -> "GetCharacterPresetsResponse":
        return cls(
            items=[
                BaseCharacterPresetResponse.from_domain(c) for c in character_presets
            ]
        )
