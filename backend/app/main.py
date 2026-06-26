import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.middleware.cors import setup_cors
from app.api.middleware.rate_limit import setup_rate_limiting
from app.api.v1.router import router
from app.core.config import settings
from app.logging.setup import setup_logging
from app.providers.ai.registry import ProviderRegistry
from app.telemetry.setup import setup_telemetry

logger = structlog.get_logger()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Open-source AI chatbot platform API",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )

    app.add_middleware(GZipMiddleware, minimum_size=1000)

    setup_cors(app)
    setup_rate_limiting(app)
    setup_logging()
    setup_telemetry(app)

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "status_code": exc.status_code,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        _request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "status_code": 500},
        )

    @app.on_event("startup")
    async def startup() -> None:
        ProviderRegistry.initialize()
        logger.info(
            "Application started",
            environment=settings.environment,
            debug=settings.debug,
        )

    @app.get("/health")
    async def health_check() -> dict:
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
        }

    @app.get("/metrics")
    async def metrics() -> dict:
        return {
            "app": settings.app_name,
            "version": settings.app_version,
            "providers": list(ProviderRegistry.get_all().keys()),
        }

    app.include_router(router)

    return app


app = create_app()
