from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.character.application.error import CharacterNotFoundError


async def character_not_found_handler(
    request: Request,
    exc: CharacterNotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


character_error_handlers = {
    CharacterNotFoundError: character_not_found_handler,
}
