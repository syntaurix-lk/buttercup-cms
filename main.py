"""
Buttercup Home Page CMS Backend
================================

Main FastAPI application entry point.

This backend service provides APIs for managing home page content
for the Buttercup restaurant website.

Features:
- CMS endpoints for all home page sections (UPSERT/REPLACE pattern)
- Full CRUD for News/Blog articles
- File upload and asset management
- Structured logging with request correlation
- Spring Boot-like DDL auto behavior via Alembic

Author: Buttercup Dev Team
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.core.logging import setup_logging, get_logger, set_request_id
from app.core.ddl import handle_ddl_auto
from app.db.session import engine
from app.api.v1 import routes_cms, routes_news, routes_assets
from app.api.v1.routes_health import router as health_router
from app.utils.api_response import api_response

import uuid
import time

# Setup logging first
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Runs on startup:
    - Handle DDL auto behavior (create/update/none)
    - Create upload directories
    - Log startup information
    
    Runs on shutdown:
    - Cleanup resources
    - Log shutdown
    """
    # Startup
    logger.info("=" * 60)
    logger.info("Buttercup CMS Backend Starting...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"DDL Auto Mode: {settings.DB_DDL_AUTO}")
    logger.info("=" * 60)
    
    # Handle database DDL based on configuration
    try:
        await handle_ddl_auto(engine, settings.DB_DDL_AUTO)
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        if settings.APP_ENV == "prod":
            raise
    
    # Ensure upload directory exists
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Upload directory ready: {upload_path.absolute()}")
    
    # Ensure logs directory exists
    log_path = Path(settings.LOG_FILE_PATH).parent
    log_path.mkdir(parents=True, exist_ok=True)
    
    logger.info("Startup complete - Ready to serve requests")
    
    yield
    
    # Shutdown
    logger.info("Buttercup CMS Backend Shutting down...")
    logger.info("Cleanup completed")


# Create FastAPI application
app = FastAPI(
    title="Buttercup Home Page CMS API",
    description="""
## Buttercup Restaurant Home Page Content Management System

This API provides endpoints for managing all content on the Buttercup restaurant home page.

### Features

* **CMS Sections** - Manage hero, about, services, testimonials, gallery, footer, and more
* **News/Blog** - Full CRUD operations for news articles
* **Assets** - Upload and manage images and files
* **Health Check** - Monitor API and database status

### Content Management Pattern

- **GET** endpoints: Retrieve content for frontend rendering
- **PUT** endpoints: Replace/upsert content (admin operations)
- **POST/PATCH/DELETE**: Full CRUD for News articles

### Notes

- No authentication required (public APIs)
- Images stored as files, URLs returned in responses
- All timestamps in UTC
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# =============================================================================
# Middleware
# =============================================================================

# CORS Middleware
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    """
    Request middleware for:
    - Request ID correlation (similar to MDC in log4j2)
    - Request timing
    - Error handling
    """
    # Generate unique request ID
    request_id = str(uuid.uuid4())[:8]
    set_request_id(request_id)
    
    # Store request ID in request state for access in routes
    request.state.request_id = request_id
    
    # Log request start
    start_time = time.time()
    logger.info(
        f"Request started",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    try:
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        # Log request completion
        logger.info(
            f"Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2)
            }
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
                "error": str(e)
            }
        )
        raise


# =============================================================================
# Exception Handlers
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=api_response(
            success=False,
            message="An internal server error occurred",
            errors=[str(exc)] if settings.DEBUG else ["Internal server error"]
        )
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 Not Found errors."""
    return JSONResponse(
        status_code=404,
        content=api_response(
            success=False,
            message=f"Resource not found: {request.url.path}",
            errors=["The requested resource does not exist"]
        )
    )


@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    """Handle validation errors with better formatting."""
    return JSONResponse(
        status_code=422,
        content=api_response(
            success=False,
            message="Validation error",
            errors=[str(exc)]
        )
    )


# =============================================================================
# Static Files
# =============================================================================

# Mount static files for serving uploaded assets
# This serves files from /uploads directory at /static/uploads URL path
app.mount(
    "/static/uploads",
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads"
)


# =============================================================================
# API Routes
# =============================================================================

# Include API routers
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    routes_cms.router,
    prefix="/api/v1/cms",
    tags=["CMS - Content Management"]
)

app.include_router(
    routes_news.router,
    prefix="/api/v1/news",
    tags=["News - Blog Articles"]
)

app.include_router(
    routes_assets.router,
    prefix="/api/v1/assets",
    tags=["Assets - File Management"]
)


# =============================================================================
# Root Endpoint
# =============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information and links.
    """
    return api_response(
        success=True,
        message="Welcome to Buttercup CMS API",
        data={
            "name": "Buttercup Home Page CMS API",
            "version": "1.0.0",
            "environment": settings.APP_ENV,
            "docs": {
                "swagger_ui": "/docs",
                "redoc": "/redoc",
                "openapi_json": "/openapi.json"
            },
            "endpoints": {
                "health": "/api/v1/health",
                "cms": "/api/v1/cms",
                "news": "/api/v1/news",
                "assets": "/api/v1/assets"
            }
        }
    )


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
