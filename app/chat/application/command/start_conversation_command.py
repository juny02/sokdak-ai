from pydantic import BaseModel
from ulid import ULID


class StartConversationCommand(BaseModel):
    character_id: ULID
    user_id: ULID
