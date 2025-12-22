from fastapi import Depends, HTTPException, status
from ulid import ULID

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
    RedisMessageRepository,
)
from app.chat.domain.enum import ConversationType
from app.chat.domain.repository import ConversationRepository, MessageRepository
from core.infra.redis.client import get_redis_client


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


def get_persistent_message_repo():
    """
    PERSISTENT 대화에서 사용되는 메시지 레포지토리를 반환합니다.
    """
    return MessageDocumentRepository()


def get_character_preset_service() -> CharacterPresetService:
    """
    CharacterPresetService 구현체 주입
    """
    return CharacterPresetService()


def get_ephemeral_message_repo():
    """
    EPHEMERAL 대화에서 사용되는 메시지 레포지토리를 반환합니다.
    """
    redis = get_redis_client()
    return RedisMessageRepository(redis=redis)


async def get_message_repo(
    conversation_id: ULID,
    conversation_repo: ConversationRepository = Depends(get_conversation_repo),
    ephemeral_message_repo: MessageRepository = Depends(get_ephemeral_message_repo),
    persistent_message_repo: MessageRepository = Depends(get_persistent_message_repo),
) -> MessageRepository:
    """
    Conversation 타입에 따라 적절한 MessageRepository를 반환한다.

    이 분기는 DI 레이어에서만 수행되며,
    UseCase 및 도메인 로직은
    메시지 저장소 종류(Redis / DB)를 알지 못한다.

    - EPHEMERAL  → RedisMessageRepository (TTL 기반)
    - PERSISTENT → DBMessageRepository
    """
    conversation = await conversation_repo.get_by_id(conversation_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    if conversation.conversation_type == ConversationType.EPHEMERAL:
        return ephemeral_message_repo

    return persistent_message_repo


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
