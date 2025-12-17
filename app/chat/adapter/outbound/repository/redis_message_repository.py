# app/chat/infrastructure/repository/redis_message_repository.py

import json
from datetime import datetime, timezone
from typing import List

from redis.asyncio import Redis
from ulid import ULID

from app.chat.domain.entity.message import Message
from app.chat.domain.enum.role import Role
from app.chat.domain.repository import MessageRepository
from core.infra.redis.keys import conversation_messages_key


class RedisMessageRepository(MessageRepository):
    """
    일회용 대화를 위해 사용하는 메세지 레포지토리 입니다.
    """

    def __init__(self, redis: Redis):
        self._redis = redis

    async def create(
        self,
        *,
        conversation_id: ULID,
        role: Role,
        content: str,
    ) -> Message:
        message = Message(
            id=ULID(),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc),
        )

        payload = {
            "id": str(message.id),
            "conversation_id": str(message.conversation_id),
            "role": message.role.value,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }

        await self._redis.rpush(
            conversation_messages_key(conversation_id),
            json.dumps(payload),
        )

        # 최초 키 생성시 24시간으로 TTL을 걸어줍니다.
        # TODO: 환경변수 관리
        if await self._redis.ttl(conversation_messages_key(conversation_id)) == -1:
            await self._redis.expire(conversation_messages_key(conversation_id), 86400)

        return message

    async def get(
        self, *, conversation_id: ULID, limit: int, before: ULID | None
    ) -> List[Message]:
        raw_items = await self._redis.lrange(
            conversation_messages_key(conversation_id),
            max(0, -limit),
            -1,
        )
        """
        Redis 기반 메시지 조회.

        - Redis LIST 구조 특성상 임의 위치 기준(`before`) 페이징은
        추가 인덱싱 없이는 비효율적이므로 현재 구현에서는 지원하지 않습니다.
        - `before` 파라미터는 무시되며,
        항상 가장 최근 메시지 `limit`개만 반환합니다.
        - 메시지는 Redis LIST에 저장된 순서를 그대로 따릅니다
        (오래된 → 최신).
        """
        messages: List[Message] = []

        for raw in raw_items:
            data = json.loads(raw)

            messages.append(
                Message(
                    id=ULID.from_str(data["id"]),
                    conversation_id=ULID.from_str(data["conversation_id"]),
                    role=Role(data["role"]),
                    content=data["content"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                )
            )

        return messages

    #  사용하지 않음
    async def delete_by_conversation_id(self, conversation_id: ULID) -> None:
        await self._redis.delete(conversation_messages_key(conversation_id))
