from pydantic import BaseModel
from ulid import ULID


class SendMessageCommand(BaseModel):
    conversation_id: ULID
    content: str
