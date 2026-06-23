import contextvars
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable to hold the correlation ID for the duration of a request
correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)


def get_correlation_id() -> str:
    """Retrieve the current request's correlation ID."""
    return correlation_id_ctx.get()


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsible solely for:
    1. Extracting or generating a unique request Correlation ID.
    2. Storing it in context variables for the duration of the request.
    3. Appending it as the 'X-Correlation-ID' response header.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # 1. Resolve Correlation ID from header or generate new one
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())

        # 2. Store in contextvars
        token = correlation_id_ctx.set(correlation_id)

        try:
            response = await call_next(request)
        finally:
            # Reset the contextvar token
            correlation_id_ctx.reset(token)

        # 3. Add to response headers
        response.headers["X-Correlation-ID"] = correlation_id
        return response
