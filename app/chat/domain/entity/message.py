from pydantic import AwareDatetime, BaseModel
from ulid import ULID

from app.chat.domain.enum.role import Role


class Message(BaseModel):
    id: ULID
    conversation_id: ULID
    role: Role
    content: str
    created_at: AwareDatetime
