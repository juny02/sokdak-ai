from pydantic import BaseModel
from ulid import ULID

from app.character.application.command.order_by import OrderBy
from app.character.domain.enum.character_type import CharacterType


class GetCharactersCommand(BaseModel):
    user_id: ULID | None = None
    type: CharacterType | None = None,
    order_by: OrderBy = OrderBy.CURR
