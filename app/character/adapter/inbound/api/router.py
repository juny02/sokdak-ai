from fastapi import APIRouter, Depends, status
from ulid import ULID

from app.character.adapter.inbound.api.schema.request import (
    PatchCharacterRequest,
    PostCharacterRequest,
)
from app.character.adapter.inbound.api.schema.response import (
    GetCharacterResponse,
    GetCharactersResponse,
    GetPersonasResponse,
    PatchCharacterResponse,
    PostCharacterResponse,
)
from app.character.application.command import (
    CreateCharacterCommand,
    GetCharactersCommand,
    OrderBy,
    UpdateCharacterCommand,
)
from app.character.application.usecase import (
    CreateCharacterUseCase,
    DeleteCharacterUseCase,
    GetCharactersUseCase,
    GetCharacterUseCase,
    GetPersonasUseCase,
    UpdateCharacterUseCase,
)
from app.character.domain.enum import CharacterType

from .dependencies import (
    get_create_character_usecase,
    get_delete_character_usecase,
    get_get_character_usecase,
    get_get_characters_usecase,
    get_get_personas_usecase,
    get_update_character_usecase,
)

router = APIRouter(prefix="/characters", tags=["Character"])


# GET /characters/personas - 각 카테고리별 키워드들을 전부 받습니다.
@router.get("/personas", response_model=GetPersonasResponse)
async def get_get_personas(
    *, usecase: GetPersonasUseCase = Depends(get_get_personas_usecase)
):
    return await usecase()


# GET /characters - 보유한 캐릭터 목록을 받습니다.
@router.get("", response_model=GetCharactersResponse)
async def get_characters(
    *,
    user_id: ULID | None = None,
    type: CharacterType | None = None,
    order_by: OrderBy = OrderBy.CURR,
    usecase: GetCharactersUseCase = Depends(get_get_characters_usecase),
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
    usecase: GetCharacterUseCase = Depends(get_get_character_usecase),
):
    character = await usecase(character_id=character_id)
    return GetCharacterResponse.from_domain(character)


# POST /characters - 캐릭터를 생성합니다.
@router.post(
    "", response_model=PostCharacterResponse, status_code=status.HTTP_201_CREATED
)
async def post_character(
    *,
    body: PostCharacterRequest,
    usecase: CreateCharacterUseCase = Depends(get_create_character_usecase),
):
    cmd = CreateCharacterCommand(**body.model_dump())
    character = await usecase(cmd)
    return PostCharacterResponse.from_domain(character)


# PATCH /characters/{character_id} - 특정 캐릭터의 이름이나 페르소나를 수정합니다.
@router.patch("/{character_id}", response_model=PatchCharacterResponse)
async def patch_character(
    *,
    character_id: ULID,
    body: PatchCharacterRequest,
    usecase: UpdateCharacterUseCase = Depends(get_update_character_usecase),
):
    cmd = UpdateCharacterCommand(**body.model_dump())
    character = await usecase(character_id=character_id, cmd=cmd)
    return PatchCharacterResponse.from_domain(character)


# DELETE /characters/{character_id} - 특정 캐릭터를 삭제합니다.
@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    *,
    character_id: ULID,
    usecase: DeleteCharacterUseCase = Depends(get_delete_character_usecase),
):
    await usecase(character_id=character_id)
