from fastapi import Depends

# Outbound (Repository Implementations)
from app.character.adapter.outbound.repository import (
    CharacterDocumentRepository,
)

# Application Layer
from app.character.application.usecase import (
    CreateCharacterUseCase,
    DeleteCharacterUseCase,
    GetCharacterPresetsUseCase,
    GetCharactersUseCase,
    GetCharacterUseCase,
    GetPersonasUseCase,
    UpdateCharacterUseCase,
)
from app.character.domain.service.character_preset_service import CharacterPresetService
from app.chat.adapter.outbound.repository import (
    ConversationDocumentRepository,
    MessageDocumentRepository,
)


# Repository Factories
def get_character_repo() -> CharacterDocumentRepository:
    """
    CharacterRepository 구현체 주입
    """
    return CharacterDocumentRepository()


def get_conversation_repo():
    """
    ConversationRepository 구현체 주입
    """
    return ConversationDocumentRepository()


def get_message_repo():
    """
    MessageRepository 구현체 주입
    """
    return MessageDocumentRepository()


def get_character_preset_service() -> CharacterPresetService:
    """
    CharacterPresetService 구현체 주입
    """
    return CharacterPresetService()


# UseCase Factories
def get_get_personas_usecase() -> GetPersonasUseCase:
    return GetPersonasUseCase()


def get_get_character_presets_usecase(service=Depends(get_character_preset_service)):
    return GetCharacterPresetsUseCase(character_preset_service=service)


def get_get_characters_usecase(repo=Depends(get_character_repo)):
    return GetCharactersUseCase(character_repo=repo)


def get_get_character_usecase(repo=Depends(get_character_repo)):
    return GetCharacterUseCase(character_repo=repo)


def get_create_character_usecase(repo=Depends(get_character_repo)):
    return CreateCharacterUseCase(character_repo=repo)


def get_update_character_usecase(repo=Depends(get_character_repo)):
    return UpdateCharacterUseCase(character_repo=repo)


def get_delete_character_usecase(
    character_repo=Depends(get_character_repo),
    conversation_repo=Depends(get_conversation_repo),
    message_repo=Depends(get_message_repo),
):
    return DeleteCharacterUseCase(
        character_repo=character_repo,
        conversation_repo=conversation_repo,
        message_repo=message_repo,
    )
