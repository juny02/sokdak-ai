from pydantic import BaseModel
from ulid import ULID

from .order_by import OrderBy


class GetConversationsCommand(BaseModel):
    user_id: ULID | None = None
    character_id: ULID | None = None
    order_by: OrderBy = OrderBy.CURR
