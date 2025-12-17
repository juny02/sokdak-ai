from datetime import datetime, timezone

from ulid import ULID

from app.chat.application.command import OrderBy
from app.chat.domain.entity.conversation import Conversation
from app.chat.domain.enum import Language
from app.chat.domain.repository import ConversationRepository


class FakeConversationRepository(ConversationRepository):
    async def create(
        self, character_id: ULID, user_id: ULID, language: Language
    ) -> Conversation:
        return Conversation(
            id=ULID(),
            character_id=character_id,
            user_id=user_id,
            summary=None,
            last_message=None,
            last_message_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            language=language,
        )

    async def get(
        self,
        order_by: OrderBy,
        user_id: ULID | None = None,
        character_id: ULID | None = None,
    ) -> list[Conversation]:
        return [
            Conversation(
                id=ULID(),
                character_id=ULID(),
                user_id=ULID(),
                summary=None,
                last_message=None,
                last_message_at=None,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                language=Language.Korean,
            )
        ]

    async def get_by_id(self, id: ULID) -> Conversation | None:
        return Conversation(
            id=id,
            character_id=ULID(),
            user_id=ULID(),
            summary=None,
            last_message=None,
            last_message_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            language=Language.Korean,
        )

    async def update(self, conversation: Conversation) -> Conversation:
        return conversation

    async def delete(self, id: ULID) -> None:
        return None

    async def get_by_character_id(self, character_id: ULID) -> Conversation | None:
        return Conversation(
            id=ULID(),
            character_id=character_id,
            user_id=ULID(),
            summary=None,
            last_message=None,
            last_message_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            language=Language.Korean,
        )
