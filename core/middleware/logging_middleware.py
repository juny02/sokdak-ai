import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.logging import get_logger

logger = get_logger("http")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        logger.info(f"--> {request.method} {request.url.path}")

        response = await call_next(request)

        duration_ms = (time.time() - start_time) * 1000
        method = request.method
        path = request.url.path
        status_code = response.status_code
        logger.info(f"<-- {method} {path} {status_code} {duration_ms:.0f}ms")

        return response
