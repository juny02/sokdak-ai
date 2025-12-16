from pydantic import BaseModel, ConfigDict

from .persona_request import PersonaRequest


class PatchCharacterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str | None = None
    persona: PersonaRequest | None = None
