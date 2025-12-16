from pydantic import BaseModel

from app.character.domain.enum import Gender, Purpose, Style, Tone
from app.character.domain.valueobject import Persona


class PersonaResponse(BaseModel):
    gender: Gender
    tone: Tone
    style: Style
    purpose: Purpose

    @classmethod
    def from_domain(cls, persona: Persona) -> "PersonaResponse":
        return cls(
            gender=persona.gender,
            tone=persona.tone,
            style=persona.style,
            purpose=persona.purpose,
        )
