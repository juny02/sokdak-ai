from dataclasses import dataclass

from app.character.domain.enum import Gender, Purpose, Style, Tone


@dataclass(frozen=True)
class Persona:
    gender: Gender  # TODO: 생김새로 변경 -> 프롬프트 영향 X
    tone: Tone
    style: Style
    purpose: Purpose
