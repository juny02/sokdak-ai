from pydantic import BaseModel
from ulid import ULID

from app.character.domain.enum import CharacterType

from .order_by import OrderBy


class GetCharactersCommand(BaseModel):
    user_id: ULID | None = None
    type: CharacterType | None = None,
    order_by: OrderBy = OrderBy.CURR
