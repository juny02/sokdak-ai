from pydantic import BaseModel
from ulid import ULID


class GetConversationsCommand(BaseModel):
    user_id: ULID | None = None
    character_id: ULID | None = None
    order_by: str = "CURR"  # 기본 값은 최근 대화한 순서
