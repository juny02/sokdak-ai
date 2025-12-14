from app.character.application.command import CreateCharacterCommand
from app.character.domain.entity import Character
from app.character.domain.repository import CharacterRepository


class CreateCharacterUseCase:
    def __init__(
        self,
        character_repo: CharacterRepository,
    ):
        self.character_repo = character_repo

    async def __call__(self, cmd: CreateCharacterCommand) -> Character:
        return await self.character_repo.create(
            user_id=cmd.user_id,
            name=cmd.name,
            persona=cmd.persona,
            type=cmd.type
        )
