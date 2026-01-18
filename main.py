"""
Buttercup Home Page CMS Backend
================================

Main FastAPI application entry point.

IMPORTANT (cPanel):
- Do NOT rely on running uvicorn on :8000 publicly.
- Use Passenger (cPanel Python App) and mount under a sub-path using ROOT_PATH.
"""

import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

# Add app to path (so "app.*" imports work)
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.core.logging import setup_logging, get_logger, set_request_id
from app.core.ddl import handle_ddl_auto
from app.db.session import engine
from app.api.v1 import routes_cms, routes_news, routes_assets, routes_auth
from app.api.v1.routes_health import router as health_router
from app.utils.api_response import api_response

# Setup logging first
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/Shutdown lifecycle."""
    logger.info("=" * 60)
    logger.info("Buttercup CMS Backend Starting...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"DDL Auto Mode: {settings.DB_DDL_AUTO}")
    logger.info(f"ROOT_PATH: {getattr(settings, 'ROOT_PATH', '') or '(none)'}")
    logger.info("=" * 60)

    # Ensure upload directory exists
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Upload directory ready: {upload_path.absolute()}")

    # Ensure logs directory exists
    log_path = Path(settings.LOG_FILE_PATH).parent
    log_path.mkdir(parents=True, exist_ok=True)

    # Handle database DDL based on configuration
    try:
        await handle_ddl_auto(engine, settings.DB_DDL_AUTO)
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # In prod, fail fast
        if settings.APP_ENV == "prod":
            raise

    logger.info("Startup complete - Ready to serve requests")
    yield

    logger.info("Buttercup CMS Backend Shutting down...")
    logger.info("Cleanup completed")


# IMPORTANT for subfolder deploy (Apache/Passenger reverse proxy)
root_path = getattr(settings, "ROOT_PATH", "") or ""

app = FastAPI(
    title="Buttercup Home Page CMS API",
    description="""
## Buttercup Restaurant Home Page Content Management System

This API provides endpoints for managing all content on the Buttercup restaurant home page.
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path=root_path,          # ✅ critical for /buttercup-cms deployments
    lifespan=lifespan,
)


# =============================================================================
# Middleware
# =============================================================================

# CORS
cors_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    """Request correlation + timing."""
    request_id = str(uuid.uuid4())[:8]
    set_request_id(request_id)
    request.state.request_id = request_id

    start_time = time.time()

    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )
        return response

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            f"Request failed: {str(e)}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration_ms, 2),
                "error": str(e),
            },
        )
        raise


# =============================================================================
# Exception Handlers
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=api_response(
            success=False,
            message="An internal server error occurred",
            errors=[str(exc)] if settings.DEBUG else ["Internal server error"],
        ),
    )


# =============================================================================
# Static Files
# =============================================================================

app.mount(
    "/static/uploads",
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads",
)

# Admin panel (static SPA)
admin_dir = Path(__file__).parent / "admin"
if admin_dir.exists():
    app.mount("/admin", StaticFiles(directory=admin_dir, html=True), name="admin")

# =============================================================================
# Routes
# =============================================================================

app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(routes_cms.router, prefix="/api/v1/cms", tags=["CMS - Content Management"])
app.include_router(routes_news.router, prefix="/api/v1/news", tags=["News - Blog Articles"])
app.include_router(routes_assets.router, prefix="/api/v1/assets", tags=["Assets - File Management"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information and links."""
    return api_response(
        success=True,
        message="Welcome to Buttercup CMS API",
        data={
            "name": "Buttercup Home Page CMS API",
            "version": "1.0.0",
            "environment": settings.APP_ENV,
            "root_path": root_path,
            "docs": {
                "swagger_ui": f"{root_path}/docs" if root_path else "/docs",
                "redoc": f"{root_path}/redoc" if root_path else "/redoc",
                "openapi_json": f"{root_path}/openapi.json" if root_path else "/openapi.json",
            },
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )
