from pydantic import BaseModel

from app.character.domain.enum import Gender, Purpose, Style, Tone


class PersonaRequest(BaseModel):
    gender: Gender
    tone: Tone
    style: Style
    purpose: Purpose
