from dataclasses import dataclass
from datetime import datetime, timezone

from ulid import ULID


@dataclass
class Conversation:
    id: ULID
    user_id: ULID
    character_id: ULID
    summary: str | None
    last_message: str | None
    last_message_at: datetime | None
    created_at: datetime
    updated_at: datetime

    def update_summary(self, summary: str) -> None:
        self.summary = summary
        self.updated_at = datetime.now(timezone.utc)

    def update_last_message(self, last_message: str) -> None:
        self.last_message = last_message
        self.updated_at = datetime.now(timezone.utc)
