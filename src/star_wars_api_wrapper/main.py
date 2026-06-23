from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from star_wars_api_wrapper.api.v1.router import api_router
from star_wars_api_wrapper.config import settings
from star_wars_api_wrapper.core.exceptions import (
    APIException,
    api_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from star_wars_api_wrapper.logger import get_logger, setup_logging
from star_wars_api_wrapper.middleware.correlation_id import CorrelationIDMiddleware
from star_wars_api_wrapper.middleware.logging import RequestLoggingMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # 1. Initialize robust logging system on startup
    setup_logging(
        log_file=settings.LOG_FILE,
        console_level=settings.LOG_LEVEL,
        file_level="DEBUG",  # Capture granular details in JSON files
        rotation_type=settings.LOG_ROTATION,
        max_bytes=settings.LOG_MAX_BYTES,
        backup_count=settings.LOG_BACKUP_COUNT,
    )
    logger.info("Starting up FastAPI application...")
    yield
    # Cleanup on shutdown
    logger.info("Shutting down FastAPI application...")


def create_app() -> FastAPI:
    """Application factory for configuring the FastAPI service."""
    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 1. Register CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Register Request Correlation & Timing Middleware
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CorrelationIDMiddleware)

    # 3. Register Custom Exception Handlers
    app.add_exception_handler(APIException, api_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # 4. Include Routers
    app.include_router(api_router, prefix="/api/v1")

    # 5. Root Redirect to API docs for user convenience
    @app.get("/", include_in_schema=False)
    async def root_redirect() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    return app


app = create_app()
