from pydantic import BaseModel

from app.chat.domain.entity import Message


class BaseMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: str

    @classmethod
    def from_domain(cls, message: Message) -> "BaseMessageResponse":
        return cls(
            id=str(message.id),
            role=message.role.value,
            content=message.content,
            created_at=message.created_at.isoformat(),
        )
