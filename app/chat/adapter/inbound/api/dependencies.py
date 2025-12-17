from fastapi import Depends
from ulid import ULID

from app.character.adapter.outbound.repository import FakeCharacterRepository
from app.character.domain.repository import CharacterRepository
from app.chat.adapter.outbound.repository import (
    FakeConversationRepository,
    FakeMessageRepository,
    RedisMessageRepository,
)
from app.chat.application.usecase import (
    DeleteConversationUseCase,
    GetConversationsUseCase,
    GetConversationUseCase,
    GetMessagesUseCase,
    SendMessageUseCase,
    StartConversationUseCase,
)
from app.chat.domain.enum import ConversationType
from app.chat.domain.repository import ConversationRepository, MessageRepository
from core.ai.client import FakeClient, OpenAIClient
from core.ai.service import LLMService, OpenAIService
from core.infra.redis.client import get_redis_client


# Repository Factories
def get_conversation_repo():
    return FakeConversationRepository()


def get_persistent_message_repo():
    """
    PERSISTENT 대화에서 사용되는 메시지 레포지토리를 반환합니다.
    """
    return FakeMessageRepository()


def get_ephemeral_message_repo():
    """
    EPHEMERAL 대화에서 사용되는 메시지 레포지토리를 반환합니다.
    """
    redis = get_redis_client()
    return RedisMessageRepository(redis=redis)


def get_character_repo():
    return FakeCharacterRepository()


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
        raise ValueError("Conversation not found")  # TODO: 적절한 예외 처리로 변경

    if conversation.conversation_type == ConversationType.EPHEMERAL:
        return ephemeral_message_repo

    return persistent_message_repo


# AI Service Factories
def get_llm_service_fake() -> LLMService:
    client = FakeClient()
    return OpenAIService(client)


def get_llm_service() -> LLMService:
    client = OpenAIClient()
    return OpenAIService(client)


# UseCase Factories


def get_start_conversation_usecase(
    repo=Depends(get_conversation_repo),
):
    return StartConversationUseCase(conversation_repo=repo)


def get_get_conversations_usecase(
    repo=Depends(get_conversation_repo),
):
    return GetConversationsUseCase(conversation_repo=repo)


def get_get_conversation_usecase(
    repo=Depends(get_conversation_repo),
):
    return GetConversationUseCase(conversation_repo=repo)


def get_delete_conversation_usecase(
    conversation_repo=Depends(get_conversation_repo),
    message_repo=Depends(get_message_repo),
):
    return DeleteConversationUseCase(
        conversation_repo=conversation_repo,
        message_repo=message_repo,
    )


async def get_get_messages_usecase(
    message_repo: MessageRepository = Depends(get_message_repo),
):
    return GetMessagesUseCase(message_repo=message_repo)


async def get_send_message_usecase(
    message_repo: MessageRepository = Depends(get_message_repo),
    conversation_repo: ConversationRepository = Depends(get_conversation_repo),
    character_repo: CharacterRepository = Depends(get_character_repo),
    llm_service: LLMService = Depends(get_llm_service_fake),
) -> SendMessageUseCase:
    return SendMessageUseCase(
        message_repo=message_repo,
        conversation_repo=conversation_repo,
        character_repo=character_repo,
        llm_service=llm_service,
    )
