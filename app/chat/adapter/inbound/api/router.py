from fastapi import APIRouter, Depends, status
from ulid import ULID

from app.chat.adapter.inbound.api.schema.request import (
    PostConversationRequest,
    PostMessageRequest,
)
from app.chat.adapter.inbound.api.schema.response import (
    GetConversationResponse,
    GetConversationsResponse,
    GetMessagesResponse,
    PostConversationResponse,
    PostMessageResponse,
)
from app.chat.application.command import (
    GetConversationsCommand,
    GetMessagesCommand,
    OrderBy,
    SendMessageCommand,
    StartConversationCommand,
)
from app.chat.application.usecase import (
    DeleteConversationUseCase,
    GetConversationsUseCase,
    GetConversationUseCase,
    GetMessagesUseCase,
    SendMessageUseCase,
    StartConversationUseCase,
)

from .dependencies import (
    get_delete_conversation_usecase,
    get_get_conversation_usecase,
    get_get_conversations_usecase,
    get_get_messages_usecase,
    get_send_message_usecase,
    get_start_conversation_usecase,
)

router = APIRouter(prefix="/conversations", tags=["Chat"])


# POST /conversations — 대화를 생성합니다.
@router.post(
    "", response_model=PostConversationResponse, status_code=status.HTTP_201_CREATED
)
async def post_conversation(
    *,
    body: PostConversationRequest,
    usecase: StartConversationUseCase = Depends(get_start_conversation_usecase),
):
    cmd = StartConversationCommand(**body.model_dump())
    conversation = await usecase(cmd)
    return PostConversationResponse.from_domain(conversation)


# GET /conversations — 대화 목록을 받습니다.
@router.get("", response_model=GetConversationsResponse)
async def get_conversations(
    *,
    user_id: ULID | None = None,
    character_id: ULID | None = None,
    order_by: OrderBy = OrderBy.CURR,
    usecase: GetConversationsUseCase = Depends(get_get_conversations_usecase),
):
    cmd = GetConversationsCommand(
        user_id=user_id,
        character_id=character_id,
        order_by=order_by,
    )
    conversations = await usecase(cmd)
    return GetConversationsResponse.from_domain(conversations)


# GET /conversations/{conversation_id} — 특정 id의 대화를 받습니다.
@router.get("/{conversation_id}", response_model=GetConversationResponse)
async def get_conversation_by_id(
    *,
    conversation_id: ULID,
    usecase: GetConversationUseCase = Depends(get_get_conversation_usecase),
):
    conversation = await usecase(conversation_id=conversation_id)
    return GetConversationResponse.from_domain(conversation)


# GET /conversations/{conversation_id}/messages — 특정 대화의 메세지들을 받습니다.
@router.get("/{conversation_id}/messages", response_model=GetMessagesResponse)
async def get_messages(
    *,
    conversation_id: ULID,
    limit: int = 20,
    before: str | None = None,
    usecase: GetMessagesUseCase = Depends(get_get_messages_usecase),
):
    cmd = GetMessagesCommand(
        conversation_id=conversation_id, limit=limit, before=before
    )
    messages = await usecase(cmd)
    return GetMessagesResponse.from_domain(messages)


# POST /conversations/{conversation_id}/messages
# 유저가 메세지를 보내고, AI의 응답을 받습니다.
@router.post("/{conversation_id}/messages", response_model=PostMessageResponse)
async def post_message(
    *,
    conversation_id: ULID,
    body: PostMessageRequest,
    usecase: SendMessageUseCase = Depends(get_send_message_usecase),
):
    cmd = SendMessageCommand(conversation_id=conversation_id, **body.model_dump())
    ai_message = await usecase(cmd)
    return PostMessageResponse.from_domain(ai_message)


# DELETE /conversations/{conversation_id} — 대화를 삭제합니다.
@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    *,
    conversation_id: ULID,
    usecase: DeleteConversationUseCase = Depends(get_delete_conversation_usecase),
):
    await usecase(conversation_id=conversation_id)
