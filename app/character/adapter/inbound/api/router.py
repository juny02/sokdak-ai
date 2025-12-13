from fastapi import APIRouter, Depends
from ulid import ULID

from app.character.adapter.inbound.api.schema.response import (
    GetCharacterResponse,
    GetCharactersResponse,
    GetPersonasResponse,
)
from app.character.application.command import GetCharactersCommand, OrderBy
from app.character.application.usecase import (
    GetCharactersUseCase,
    GetCharacterUseCase,
    GetPersonasUseCase,
)
from app.character.domain.enum import CharacterType

from .dependencies import (
    get_get_character_usecase,
    get_get_characters_usecase,
    get_get_personas_usecase,
)

router = APIRouter(prefix="/characters", tags=["Character"])


# GET /characters/personas - 각 카테고리별 키워드들을 전부 받습니다.
@router.get("/personas", response_model=GetPersonasResponse)
async def get_get_personas(
    *,
    usecase: GetPersonasUseCase = Depends(get_get_personas_usecase)
):
    return await usecase()


# GET /characters - 보유한 캐릭터 목록을 받습니다.
@router.get("", response_model=GetCharactersResponse)
async def get_characters(
    *,
    user_id: ULID | None = None,
    type: CharacterType | None = None,
    order_by: OrderBy = OrderBy.CURR,
    usecase: GetCharactersUseCase = Depends(get_get_characters_usecase)
):
    cmd = GetCharactersCommand(
        user_id=user_id,
        type=type,
        order_by=order_by,
    )
    characters = await usecase(cmd)
    return GetCharactersResponse.from_domain(characters)


# GET /characters/{character_id} - 특정 id의 캐릭터를 받습니다.
@router.get("/{character_id}", response_model=GetCharacterResponse)
async def get_character_by_id(
    *,
    character_id: ULID,
    usecase: GetCharacterUseCase = Depends(get_get_character_usecase)
):
    character = await usecase(character_id=character_id)
    return GetCharacterResponse.from_domain(character)
