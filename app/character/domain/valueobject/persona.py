from dataclasses import dataclass

from app.character.domain.enum import Purpose, Style, Tone


@dataclass(frozen=True)
class Persona:
    tone: Tone
    style: Style
    purpose: Purpose
