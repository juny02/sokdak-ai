from fastapi import Depends

# Outbound (Repository Implementations)
from app.character.adapter.outbound.repository import (
    FakeCharacterRepository,
)

# Application Layer
from app.character.application.usecase import (
    GetCharactersUseCase,
    GetPersonasUseCase,
)


# Repository Factories
def get_character_repo():
    """
    CharacterRepository 구현체 주입
    """
    return FakeCharacterRepository()

# UseCase Factories


def get_personas_usecase() -> GetPersonasUseCase:
    return GetPersonasUseCase()


def get_get_characters_usecase(
    repo=Depends(get_character_repo)
):
    return GetCharactersUseCase(character_repo=repo)
