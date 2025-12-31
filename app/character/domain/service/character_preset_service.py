from app.character.domain.enum import Gender, Purpose, Style, Tone

from ..valueobject.character_preset import CharacterPreset
from ..valueobject.persona import Persona


class CharacterPresetService:
    def get(self) -> list[CharacterPreset]:
        return [
            CharacterPreset(
                key="nun",
                name="수녀님",
                description="차분하고 따뜻하게 조언해주는 수녀님",
                persona=Persona(
                    gender=Gender.FEMALE,
                    tone=Tone.CALM,
                    style=Style.LISTENER,
                    purpose=Purpose.COUNSELING,
                ),
            ),
            CharacterPreset(
                key="friend",
                name="친구",
                description="편하게 수다 떨 수 있는 친구",
                persona=Persona(
                    gender=Gender.NEUTRAL,
                    tone=Tone.FRIENDLY,
                    style=Style.EMPATHETIC,
                    purpose=Purpose.CASUAL_CHAT,
                ),
            ),
        ]
