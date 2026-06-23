import logging
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class APIException(Exception):
    """Base exception class for all custom application errors."""

    def __init__(
        self,
        detail: str,
        status_code: int = 400,
        code: str = "BAD_REQUEST",
        details: Any = None,
    ) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        self.code = code
        self.details = details


class NotFoundException(APIException):
    """Error raised when a requested resource is not found."""

    def __init__(
        self,
        detail: str = "Resource not found",
        code: str = "NOT_FOUND",
    ) -> None:
        super().__init__(detail=detail, status_code=404, code=code)


class BadRequestException(APIException):
    """Error raised for client errors / bad input parameters."""

    def __init__(
        self,
        detail: str = "Bad request",
        code: str = "BAD_REQUEST",
    ) -> None:
        super().__init__(detail=detail, status_code=400, code=code)


class UnauthorizedException(APIException):
    """Error raised when credentials validation fails."""

    def __init__(
        self,
        detail: str = "Unauthorized",
        code: str = "UNAUTHORIZED",
    ) -> None:
        super().__init__(detail=detail, status_code=401, code=code)


class ForbiddenException(APIException):
    """Error raised when action is not permitted for the user."""

    def __init__(
        self,
        detail: str = "Forbidden",
        code: str = "FORBIDDEN",
    ) -> None:
        super().__init__(detail=detail, status_code=403, code=code)


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """Handles all APIException errors and returns structured error JSON."""
    content = {
        "success": False,
        "code": exc.code,
        "message": exc.detail,
    }
    if exc.details is not None:
        content["details"] = exc.details

    return JSONResponse(status_code=exc.status_code, content=content)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles FastAPI parameter validation errors and returns structured details."""
    errors = []
    for error in exc.errors():
        # Clean up path locations (tuples) into strings
        loc = " -> ".join(str(x) for x in error["loc"] if x != "body")
        errors.append(
            {
                "field": loc or "payload",
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "code": "VALIDATION_ERROR",
            "message": "Validation failed for request parameters or payload.",
            "details": errors,
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected code-level exceptions."""
    # Ensure trace is captured inside application log files
    logger.exception(
        f"Unhandled system error occurred: {exc} | Path: {request.url.path}",
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please contact support.",
        },
    )
