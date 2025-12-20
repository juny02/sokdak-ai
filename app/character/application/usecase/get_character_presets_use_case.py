from app.character.domain.service import CharacterPresetService
from app.character.domain.valueobject import CharacterPreset


class GetCharacterPresetsUseCase:
    """
    기본 캐릭터들을 반환합니다.
    """

    def __init__(self, character_preset_service: CharacterPresetService):
        self.service = character_preset_service

    # TODO: DB 연결하는거 아니면 굳이 async안써도 됨??
    async def __call__(self) -> list[CharacterPreset]:
        return self.service.get()
