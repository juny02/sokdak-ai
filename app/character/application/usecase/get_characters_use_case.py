from app.character.application.command.get_characters_command import (
    GetCharactersCommand,
)
from app.character.domain.entity import Character
from app.character.domain.repository import CharacterRepository


class GetCharactersUseCase:
    """
    유저가 생성한 캐릭터들을 반환합니다.
    """

    def __init__(
        self,
        character_repo: CharacterRepository,
    ):
        self.character_repo = character_repo

    async def __call__(self, cmd: GetCharactersCommand) -> list[Character]:
        return await self.character_repo.get(
            user_id=cmd.user_id,
            order_by=cmd.order_by,
            type=cmd.type,
        )
