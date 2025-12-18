from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.chat.application.error import ConversationNotFoundError


async def conversation_not_found_handler(
    request: Request,
    exc: ConversationNotFoundError,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


chat_error_handlers = {
    ConversationNotFoundError: conversation_not_found_handler,
}
