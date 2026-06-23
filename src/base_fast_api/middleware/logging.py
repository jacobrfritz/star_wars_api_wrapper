import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsible solely for:
    1. Logging request arrival metadata (method, path, client IP).
    2. Logging request completion status and execution duration (ms).
    3. Logging details of unhandled processing exceptions.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()

        # 1. Log request entry
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_host": request.client.host if request.client else None,
            },
        )

        try:
            response = await call_next(request)
        except Exception as e:
            # Log failure if processing raises an unhandled error
            duration = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"Request failed: {request.method} {request.url.path} - Error: {e}",
                extra={
                    "duration_ms": round(duration, 2),
                    "status_code": 500,
                },
                exc_info=e,
            )
            raise e

        # 2. Log request completion
        duration = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"Finished request: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.2f}ms",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration, 2),
            },
        )

        return response
