from typing import Dict, List

from app.character.domain.valueobject.persona import Gender, Purpose, Style, Tone


class GetPersonasUseCase:
    """
    페르소나 키워드 전체를 반환합니다.
    """

    def __init__(self) -> None:
        pass

    async def __call__(self) -> Dict[str, List[str]]:
        """
        각 카테고리별 페르소나 키워드 전체를 반환합니다.
        """
        return {
            "gender": [g.value for g in Gender],
            "tone": [t.value for t in Tone],
            "style": [s.value for s in Style],
            "purpose": [p.value for p in Purpose],
        }
