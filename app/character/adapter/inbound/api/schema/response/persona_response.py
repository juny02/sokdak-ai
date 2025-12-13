from pydantic import BaseModel

from app.character.domain.valueobject.persona import (
    Gender,
    Persona,
    Purpose,
    Style,
    Tone,
)


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
            purpose=persona.purpose
        )
