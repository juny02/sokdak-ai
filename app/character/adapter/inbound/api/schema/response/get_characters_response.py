from pydantic import BaseModel

from app.character.domain.entity import Character

from .base_character_response import BaseCharacterResponse


class GetCharactersResponse(BaseModel):
    items: list[BaseCharacterResponse]

    # Domain 객체를 API Response 모델로 변환하는 팩토리 메서드다.
    @classmethod
    def from_domain(cls, characters: list[Character]) -> "GetCharactersResponse":
        return cls(items=[BaseCharacterResponse.from_domain(c) for c in characters])
