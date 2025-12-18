from datetime import datetime, timezone

from ulid import ULID

from app.chat.adapter.outbound.entity.conversation_document import ConversationDocument
from app.chat.adapter.outbound.mapper.conversation_mapper import ConversationMapper
from app.chat.application.command import OrderBy
from app.chat.domain.entity.conversation import Conversation
from app.chat.domain.enum import ConversationType, Language
from app.chat.domain.repository import ConversationRepository


class ConversationDocumentRepository(ConversationRepository):
    """
    MongoDB / Beanie 구현체
    """

    async def create(
        self,
        character_id: ULID,
        user_id: ULID,
        language: Language,
        conversation_type: ConversationType,
    ) -> Conversation:
        now = datetime.now(timezone.utc)

        doc = ConversationDocument(
            user_id=user_id,
            character_id=character_id,
            language=language,
            conversation_type=conversation_type,
            summary=None,
            last_message=None,
            last_message_at=None,
            created_at=now,
            updated_at=now,
        )

        await doc.insert()
        return ConversationMapper.to_domain(doc)

    async def get(
        self,
        order_by: OrderBy,
        user_id: ULID | None,
        character_id: ULID | None,
    ) -> list[Conversation]:
        conditions = []

        if user_id is not None:
            conditions.append(ConversationDocument.user_id == user_id)

        if character_id is not None:
            conditions.append(ConversationDocument.character_id == character_id)

        query = ConversationDocument.find(*conditions)

        sort_mapping: dict[OrderBy, str] = {
            OrderBy.CURR: "-created_at",  # 최신 생성순 (default)
            OrderBy.ASC: "created_at",  # 오래된 생성순
            OrderBy.DESC: "-last_chat_at",  # 최근 대화순
        }

        query = query.sort(sort_mapping[order_by])

        docs = await query.to_list()
        return [ConversationMapper.to_domain(doc) for doc in docs]

    async def get_by_id(self, id: ULID) -> Conversation | None:
        doc = await ConversationDocument.get(id)
        if doc is None:
            return None
        return ConversationMapper.to_domain(doc)

    async def update(self, conversation: Conversation) -> Conversation:
        doc = await ConversationDocument.get(conversation.id)

        doc.summary = conversation.summary
        doc.last_message = conversation.last_message
        doc.last_message_at = conversation.last_message_at
        doc.updated_at = conversation.updated_at
        doc.language = conversation.language
        doc.conversation_type = conversation.conversation_type

        await doc.save()
        return ConversationMapper.to_domain(doc)

    async def delete(self, id: ULID) -> None:
        doc = await ConversationDocument.get(id)
        if doc is not None:
            await doc.delete()

    async def get_by_character_id(self, character_id: ULID) -> Conversation | None:
        doc = await ConversationDocument.find_one(
            ConversationDocument.character_id == character_id
        )
        if doc is None:
            return None
        return ConversationMapper.to_domain(doc)
