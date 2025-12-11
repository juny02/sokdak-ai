# app/chat/adapter/inbound/api/dependencies.py

from fastapi import Depends

# Outbound (Repository Implementations)
from app.chat.adapter.outbound.repository import (
    FakeConversationRepository,
    FakeMessageRepository,
)

# Application Layer
from app.chat.application.usecase import (
    DeleteConversationUseCase,
    GetConversationsUseCase,
    GetConversationUseCase,
    GetMessagesUseCase,
    SendMessageUseCase,
    StartConversationUseCase,
)

# Repository Factories


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


# ----------------------------
# UseCase Factories
# ----------------------------


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
):
    return SendMessageUseCase(
        message_repo=message_repo,
        conversation_repo=conversation_repo,
    )
