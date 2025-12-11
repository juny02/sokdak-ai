from pydantic import BaseModel

from app.chat.domain.entity import Message

from .base_message_response import BaseMessageResponse


class GetMessagesResponse(BaseModel):
    items: list[BaseMessageResponse]
    next_cursor: str | None = None

    @classmethod
    def from_domain(cls, messages: list[Message]):
        # 가장 마지막 요소를 next_cursor로 설정
        cursor = str(messages[-1].id) if messages else None
        return cls(
            items=[BaseMessageResponse.from_domain(m) for m in messages],
            next_cursor=cursor,
        )
