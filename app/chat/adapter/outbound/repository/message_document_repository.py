from datetime import datetime, timezone

from ulid import ULID

from app.chat.adapter.outbound.entity.message_document import MessageDocument
from app.chat.adapter.outbound.mapper.message_mapper import MessageMapper
from app.chat.domain.entity import Message
from app.chat.domain.enum import Role
from app.chat.domain.repository import MessageRepository


class MessageDocumentRepository(MessageRepository):
    """
    MongoDB / Beanie 기반 MessageRepository 구현체
    """

    async def create(
        self,
        conversation_id: ULID,
        role: Role,
        content: str,
    ) -> Message:
        now = datetime.now(timezone.utc)

        doc = MessageDocument(
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=now,
        )

        await doc.insert()
        return MessageMapper.to_domain(doc)

    async def get(
        self,
        conversation_id: ULID,
        limit: int,
        before: ULID | None,
    ) -> list[Message]:
        """
        특정 conversation의 메시지 목록 조회
        - 최신 메시지부터 과거 방향
        - before가 있으면 해당 메시지 이전 것들만 조회
        """
        conditions = [MessageDocument.conversation_id == conversation_id]

        if before is not None:
            # ULID는 시간순 정렬 가능 → cursor paging에 적합
            conditions.append(MessageDocument.id < before)

        query = (
            MessageDocument.find(*conditions)
            .sort(-MessageDocument.created_at)
            .limit(limit)
        )

        docs = await query.to_list()
        return [MessageMapper.to_domain(doc) for doc in docs]

    async def delete_by_conversation_id(self, conversation_id: ULID) -> None:
        await MessageDocument.find(
            MessageDocument.conversation_id == conversation_id
        ).delete()
