from app.character.domain.enum import Appearance, Purpose, Style, Tone

from ..valueobject.character_preset import CharacterPreset
from ..valueobject.persona import Persona


class CharacterPresetService:
    def get(self) -> list[CharacterPreset]:
        return [
            CharacterPreset(
                key="priest",
                name="신부님",
                description="차분하고 따뜻하게 고해를 들어주는 신부님",
                persona=Persona(
                    tone=Tone.CALM,
                    style=Style.LISTENER,
                    purpose=Purpose.CONFESSION,
                ),
                appearance=Appearance.PRIEST,
            ),
            CharacterPreset(
                key="friend",
                name="친구",
                description="편하게 수다 떨 수 있는 친구",
                persona=Persona(
                    tone=Tone.FRIENDLY,
                    style=Style.EMPATHETIC,
                    purpose=Purpose.CASUAL_CHAT,
                ),
                appearance=Appearance.FRIEND,
            ),
        ]
