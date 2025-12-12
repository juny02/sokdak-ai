from pydantic import BaseModel
from ulid import ULID


class GetMessagesCommand(BaseModel):
    conversation_id: ULID
    limit: int
    before: ULID | None = None  # 페이징 커서. 해당 id 이전 메시지를 조회함
