from fastapi import APIRouter, Depends

from app.character.adapter.inbound.api.schema.response.get_personas_response import (
    GetPersonasResponse,
)
from app.character.application.usecase import GetPersonasUseCase

from .dependencies import (
    get_personas_usecase,
)

router = APIRouter(prefix="/characters", tags=["Character"])


# GET /characters/personas - 각 카테고리별 키워드들을 전부 받습니다.
@router.get("/personas", response_model=GetPersonasResponse)
async def get_personas(
    usecase: GetPersonasUseCase = Depends(get_personas_usecase)
):
    return await usecase()
