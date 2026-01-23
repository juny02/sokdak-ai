from pydantic import BaseModel

from app.character.domain.enum import Purpose, Style, Tone


class PersonaRequest(BaseModel):
    tone: Tone
    style: Style
    purpose: Purpose
