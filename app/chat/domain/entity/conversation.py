from datetime import datetime, timezone

from pydantic import AwareDatetime, BaseModel
from ulid import ULID


class Conversation(BaseModel):
    id: ULID
    user_id: ULID
    character_id: ULID
    summary: str | None
    last_message: str | None
    last_message_at: AwareDatetime | None
    created_at: AwareDatetime
    updated_at: AwareDatetime

    def update_summary(self, summary: str) -> None:
        self.summary = summary
        self.updated_at = datetime.now(timezone.utc)

    def update_last_message(self, last_message: str) -> None:
        self.last_message = last_message
        self.updated_at = datetime.now(timezone.utc)
