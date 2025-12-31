from dataclasses import dataclass

from ..valueobject.persona import Persona


@dataclass(frozen=True)
class CharacterPreset:
    key: str
    name: str
    description: str
    persona: Persona
