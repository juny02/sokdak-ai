from pydantic import BaseModel

from app.character.domain.valueobject import Persona


class UpdateCharacterCommand(BaseModel):
    """
    캐릭터를 수정하기 위한 Command
    """

    name: str | None = None
    persona: Persona | None = None
