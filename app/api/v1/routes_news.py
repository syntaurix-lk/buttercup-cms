"""
News API Routes
===============

Full CRUD endpoints for news/blog articles.

PUBLIC ENDPOINTS:
- GET /news - List published articles
- GET /news/{slug} - Get article by slug

ADMIN ENDPOINTS (no auth):
- POST /news - Create article
- GET /news/admin - List all articles (including drafts)
- GET /news/admin/{id} - Get article by ID
- PATCH /news/{id} - Update article
- DELETE /news/{id} - Delete article
- PATCH /news/{id}/publish - Publish article
- PATCH /news/{id}/unpublish - Unpublish article
"""

import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.news_service import NewsService
from app.utils.api_response import success_response, error_response
from app.schemas.news import (
    NewsCreate,
    NewsUpdate,
    NewsResponse,
    NewsListResponse,
    NewsPublishAction,
)

router = APIRouter()


def get_news_service(db: Session = Depends(get_db)) -> NewsService:
    """Dependency to get news service instance."""
    return NewsService(db)


# =============================================================================
# Public Endpoints
# =============================================================================

@router.get("", response_model=dict, summary="List published news")
def list_published_news(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    service: NewsService = Depends(get_news_service)
):
    """
    List published news articles for public view.
    
    Supports pagination and category filtering.
    """
    articles, total = service.list_published(page, page_size, category)
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    response_data = NewsListResponse(
        items=[NewsResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
    
    return success_response(data=response_data.model_dump())


@router.get("/categories", response_model=dict, summary="List news categories")
def list_categories(service: NewsService = Depends(get_news_service)):
    """Get list of all news categories."""
    categories = service.get_categories()
    return success_response(data=categories)


@router.get("/{slug}", response_model=dict, summary="Get news by slug")
def get_news_by_slug(
    slug: str,
    service: NewsService = Depends(get_news_service)
):
    """
    Get a published news article by its slug.
    
    Also increments view count.
    """
    article = service.get_by_slug(slug)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if not article.is_published:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Increment view count
    service.increment_view_count(article.id)
    
    return success_response(data=NewsResponse.model_validate(article).model_dump())


# =============================================================================
# Admin Endpoints
# =============================================================================

@router.post("", response_model=dict, summary="Create news article")
def create_news(
    data: NewsCreate,
    service: NewsService = Depends(get_news_service)
):
    """Create a new news article."""
    article = service.create(data)
    return success_response(
        data=NewsResponse.model_validate(article).model_dump(),
        message="Article created successfully"
    )


@router.get("/admin/list", response_model=dict, summary="List all news (admin)")
def list_all_news(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_published: Optional[bool] = Query(None, description="Filter by published status"),
    service: NewsService = Depends(get_news_service)
):
    """
    List all news articles including drafts (for admin).
    
    Supports pagination and filtering by category and publish status.
    """
    articles, total = service.list_all(page, page_size, category, is_published)
    
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    response_data = NewsListResponse(
        items=[NewsResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
    
    return success_response(data=response_data.model_dump())


@router.get("/admin/{news_id}", response_model=dict, summary="Get news by ID (admin)")
def get_news_by_id(
    news_id: int,
    service: NewsService = Depends(get_news_service)
):
    """Get a news article by ID (for admin, includes drafts)."""
    article = service.get_by_id(news_id)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return success_response(data=NewsResponse.model_validate(article).model_dump())


@router.patch("/{news_id}", response_model=dict, summary="Update news article")
def update_news(
    news_id: int,
    data: NewsUpdate,
    service: NewsService = Depends(get_news_service)
):
    """Update a news article (partial update supported)."""
    article = service.update(news_id, data)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return success_response(
        data=NewsResponse.model_validate(article).model_dump(),
        message="Article updated successfully"
    )


@router.delete("/{news_id}", response_model=dict, summary="Delete news article")
def delete_news(
    news_id: int,
    service: NewsService = Depends(get_news_service)
):
    """Delete a news article."""
    deleted = service.delete(news_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return success_response(message="Article deleted successfully")


@router.patch("/{news_id}/publish", response_model=dict, summary="Publish news article")
def publish_news(
    news_id: int,
    data: NewsPublishAction = None,
    service: NewsService = Depends(get_news_service)
):
    """Publish a news article."""
    published_at = data.published_at if data else None
    article = service.publish(news_id, published_at)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return success_response(
        data=NewsResponse.model_validate(article).model_dump(),
        message="Article published successfully"
    )


@router.patch("/{news_id}/unpublish", response_model=dict, summary="Unpublish news article")
def unpublish_news(
    news_id: int,
    service: NewsService = Depends(get_news_service)
):
    """Unpublish a news article."""
    article = service.unpublish(news_id)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return success_response(
        data=NewsResponse.model_validate(article).model_dump(),
        message="Article unpublished successfully"
    )
