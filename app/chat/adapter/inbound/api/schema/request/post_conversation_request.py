from pydantic import BaseModel, ConfigDict
from ulid import ULID


class PostConversationRequest(BaseModel):
    # 정의되지 않은 필드 허용 안 함, 인스턴스 불변
    model_config = ConfigDict(extra="forbid", frozen=True)

    character_id: ULID
    user_id: ULID
