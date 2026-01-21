from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.chat.application.error import ConversationNotFoundError
from core.logging import get_logger

logger = get_logger("chat.error")


async def conversation_not_found_handler(
    request: Request,
    exc: ConversationNotFoundError,
):
    logger.error(f"{exc.__class__.__name__}: {exc} | path={request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


chat_error_handlers = {
    ConversationNotFoundError: conversation_not_found_handler,
}
