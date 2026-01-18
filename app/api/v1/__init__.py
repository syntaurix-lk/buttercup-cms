"""
API v1 Package
==============

Aggregates all v1 API routers.
"""

from fastapi import APIRouter

from app.api.v1.routes_cms import router as cms_router
from app.api.v1.routes_news import router as news_router
from app.api.v1.routes_assets import router as assets_router
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_auth import router as auth_router

# Create main v1 router
api_router = APIRouter()

# Include all route modules
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(cms_router, prefix="/cms", tags=["CMS"])
api_router.include_router(news_router, prefix="/news", tags=["News"])
api_router.include_router(assets_router, prefix="/assets", tags=["Assets"])
