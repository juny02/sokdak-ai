from fastapi import Depends

# Outbound (Repository Implementations)
from app.character.adapter.outbound.repository import (
    FakeCharacterRepository,
)

# Application Layer
from app.character.application.usecase import (
    CreateCharacterUseCase,
    DeleteCharacterUseCase,
    GetCharactersUseCase,
    GetCharacterUseCase,
    GetPersonasUseCase,
    UpdateCharacterUseCase,
)
from app.chat.adapter.outbound.repository import (
    FakeConversationRepository,
    FakeMessageRepository,
)


# Repository Factories
def get_character_repo():
    """
    CharacterRepository 구현체 주입
    """
    return FakeCharacterRepository()


def get_conversation_repo():
    """
    ConversationRepository 구현체 주입
    """
    return FakeConversationRepository()


def get_message_repo():
    """
    MessageRepository 구현체 주입
    """
    return FakeMessageRepository()


# UseCase Factories
def get_get_personas_usecase() -> GetPersonasUseCase:
    return GetPersonasUseCase()


def get_get_characters_usecase(
    repo=Depends(get_character_repo)
):
    return GetCharactersUseCase(character_repo=repo)


def get_get_character_usecase(
    repo=Depends(get_character_repo)
):
    return GetCharacterUseCase(character_repo=repo)


def get_create_character_usecase(
    repo=Depends(get_character_repo)
):
    return CreateCharacterUseCase(character_repo=repo)


def get_update_character_usecase(
    repo=Depends(get_character_repo)
):
    return UpdateCharacterUseCase(character_repo=repo)


def get_delete_character_usecase(
    character_repo=Depends(get_character_repo),
    conversation_repo=Depends(get_conversation_repo),
    message_repo=Depends(get_message_repo)
):
    return DeleteCharacterUseCase(
        character_repo=character_repo,
        conversation_repo=conversation_repo,
        message_repo=message_repo
    )
