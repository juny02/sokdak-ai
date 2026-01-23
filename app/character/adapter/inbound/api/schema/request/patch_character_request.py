from pydantic import BaseModel, ConfigDict

from app.character.domain.enum import Appearance

from .persona_request import PersonaRequest


class PatchCharacterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str | None = None
    persona: PersonaRequest | None = None
    appearance: Appearance | None = None
