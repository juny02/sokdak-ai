from dataclasses import dataclass

from app.character.domain.enum import Gender, Purpose, Style, Tone


@dataclass(frozen=True)
class Persona:
    gender: Gender
    tone: Tone
    style: Style
    purpose: Purpose
