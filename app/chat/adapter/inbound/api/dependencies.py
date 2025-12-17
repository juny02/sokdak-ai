from fastapi import Depends

from app.character.adapter.outbound.repository import FakeCharacterRepository
from app.chat.adapter.outbound.repository import (
    FakeConversationRepository,
    FakeMessageRepository,
)
from app.chat.application.usecase import (
    DeleteConversationUseCase,
    GetConversationsUseCase,
    GetConversationUseCase,
    GetMessagesUseCase,
    SendMessageUseCase,
    StartConversationUseCase,
)
from core.ai.client import FakeClient, OpenAIClient
from core.ai.service import LLMService, OpenAIService


# Repository Factories
def get_conversation_repo():
    return FakeConversationRepository()


def get_message_repo():
    return FakeMessageRepository()


def get_character_repo():
    return FakeCharacterRepository()


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


def get_get_messages_usecase(
    repo=Depends(get_message_repo),
):
    return GetMessagesUseCase(message_repo=repo)


def get_send_message_usecase(
    message_repo=Depends(get_message_repo),
    conversation_repo=Depends(get_conversation_repo),
    character_repo=Depends(get_character_repo),
    llm_service=Depends(get_llm_service_fake),
):
    return SendMessageUseCase(
        message_repo=message_repo,
        conversation_repo=conversation_repo,
        character_repo=character_repo,
        llm_service=llm_service,
    )
