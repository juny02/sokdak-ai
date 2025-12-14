from dataclasses import dataclass
from datetime import datetime

from ulid import ULID

from app.chat.domain.enum.role import Role


@dataclass
class Message:
    id: ULID
    conversation_id: ULID
    role: Role
    content: str
    created_at: datetime
