from contextlib import asynccontextmanager

import logging

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.customers import router as customers_router
from app.api.v1.auth import router as auth_router
from app.api.v1.orders import router as orders_router
from app.api.v1.products import router as products_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.triggers import router as triggers_router
from app.api.v1.users import router as users_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.middleware.request_logging import RequestLoggingMiddleware


logger = get_logger(__name__)
api_router = APIRouter(prefix=settings.api_v1_prefix)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Application lifecycle hook.

    This stays intentionally lightweight in the first file so future
    configuration, logging, and database initialization can be added
    without changing the public entrypoint.
    """
    configure_logging()
    logger.info("Starting application in %s mode", settings.environment)
    yield
    logger.info("Stopping application")


@api_router.get("/health", tags=["Health"], summary="Versioned health check")
async def versioned_health_check() -> dict[str, str]:
    return {"status": "ok", "version": "v1"}


def _register_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled application error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )


def create_application() -> FastAPI:
    """
    Build and configure the FastAPI application instance.

    The app factory pattern keeps startup logic testable and makes it easy
    to compose environment-specific settings in later files.
    """
    application = FastAPI(
        title=settings.project_name,
        description=settings.project_description,
        version=settings.project_version,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url=f"{settings.api_v1_prefix}/docs",
        redoc_url=f"{settings.api_v1_prefix}/redoc",
        lifespan=lifespan,
    )

    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _register_exception_handlers(application)

    @application.get("/health", tags=["Health"], summary="Health check")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    application.include_router(api_router)
    application.include_router(auth_router, prefix=settings.api_v1_prefix)
    application.include_router(users_router, prefix=settings.api_v1_prefix)
    application.include_router(customers_router, prefix=settings.api_v1_prefix)
    application.include_router(products_router, prefix=settings.api_v1_prefix)
    application.include_router(orders_router, prefix=settings.api_v1_prefix)
    application.include_router(tasks_router, prefix=settings.api_v1_prefix)
    application.include_router(triggers_router, prefix=settings.api_v1_prefix)

    return application


app = create_application()
