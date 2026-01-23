from ulid import ULID

from app.character.application.command import UpdateCharacterCommand
from app.character.application.error import CharacterNotFoundError
from app.character.domain.entity import Character
from app.character.domain.repository import CharacterRepository


class UpdateCharacterUseCase:
    """
    캐릭터의 이름이나 페르소나를 변경합니다.

    흐름:
        1) 캐릭터 조회
        2) 이름|페르소나|외형 변경
        3) 저장
    """

    def __init__(
        self,
        character_repo: CharacterRepository,
    ):
        self.character_repo = character_repo

    async def __call__(
        self, character_id: ULID, cmd: UpdateCharacterCommand
    ) -> Character:
        # 1) 캐릭터 조회
        character = await self.character_repo.get_by_id(character_id)

        if not character:
            raise CharacterNotFoundError()

        # 2) Command에 포함된 값만 선택적으로 반영
        if cmd.name is not None:
            character.update_name(cmd.name)

        if cmd.persona is not None:
            character.update_persona(cmd.persona)

        if cmd.appearance is not None:
            character.update_appearance(cmd.appearance)

        # 3) 변경된 캐릭터의 최종 상태를 저장소에 반영
        await self.character_repo.update(character)

        return character
