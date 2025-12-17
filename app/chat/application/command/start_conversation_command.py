from pydantic import BaseModel
from ulid import ULID

from app.chat.domain.enum import Language


class StartConversationCommand(BaseModel):
    character_id: ULID
    user_id: ULID
    language: Language
