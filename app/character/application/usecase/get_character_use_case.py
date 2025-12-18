from ulid import ULID

from app.character.application.error import CharacterNotFoundError
from app.character.domain.entity import Character
from app.character.domain.repository import CharacterRepository


class GetCharacterUseCase:
    def __init__(
        self,
        character_repo: CharacterRepository,
    ):
        self.character_repo = character_repo

    # usecase에서는 항상 성공 결과만을 반환하고, 반환값이 없으면 의미있는 예외로 표현
    async def __call__(self, character_id: ULID) -> Character:
        character = await self.character_repo.get_by_id(id=character_id)

        if not character:
            raise CharacterNotFoundError()

        return character
