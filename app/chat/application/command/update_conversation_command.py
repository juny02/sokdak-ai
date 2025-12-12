from pydantic import BaseModel
from ulid import ULID


class UpdateConversationCommand(BaseModel):
    """
    대화의 요약 및 마지막 메시지를 수정하기 위한 Command.
    """

    conversation_id: ULID
    summary: str | None = None
    last_message: str | None = None
