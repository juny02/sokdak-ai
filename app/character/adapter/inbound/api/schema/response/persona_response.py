from pydantic import BaseModel

from app.character.domain.enum import Purpose, Style, Tone
from app.character.domain.valueobject import Persona


class PersonaResponse(BaseModel):
    tone: Tone
    style: Style
    purpose: Purpose

    @classmethod
    def from_domain(cls, persona: Persona) -> "PersonaResponse":
        return cls(
            tone=persona.tone,
            style=persona.style,
            purpose=persona.purpose,
        )
