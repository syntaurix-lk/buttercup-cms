"""
News/Blog Schemas
=================

Pydantic schemas for news/blog article validation.
Supports full CRUD operations.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from slugify import slugify


class NewsBase(BaseModel):
    """Base news schema."""
    title: str = Field(..., min_length=1, max_length=500)
    summary: Optional[str] = None
    content: Optional[str] = None
    cover_image_path: Optional[str] = Field(default=None, max_length=500)
    author: Optional[str] = Field(default="Admin", max_length=255)
    category: Optional[str] = Field(default=None, max_length=100)
    tags: Optional[str] = Field(default=None, max_length=500)
    meta_title: Optional[str] = Field(default=None, max_length=255)
    meta_description: Optional[str] = None


class NewsCreate(NewsBase):
    """Schema for creating news articles."""
    slug: Optional[str] = Field(default=None, max_length=191)
    is_published: bool = False
    published_at: Optional[datetime] = None
    
    @field_validator("slug", mode="before")
    @classmethod
    def generate_slug(cls, v, info):
        """Generate slug from title if not provided."""
        if v:
            return slugify(v)[:191]
        # Will be generated in service if title available
        return v


class NewsUpdate(BaseModel):
    """Schema for updating news articles (partial update)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    slug: Optional[str] = Field(default=None, max_length=191)
    summary: Optional[str] = None
    content: Optional[str] = None
    cover_image_path: Optional[str] = Field(default=None, max_length=500)
    author: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, max_length=100)
    tags: Optional[str] = Field(default=None, max_length=500)
    is_published: Optional[bool] = None
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = Field(default=None, max_length=255)
    meta_description: Optional[str] = None
    
    @field_validator("slug", mode="before")
    @classmethod
    def slugify_slug(cls, v):
        """Slugify the slug if provided."""
        if v:
            return slugify(v)[:191]
        return v


class NewsResponse(NewsBase):
    """Schema for news response."""
    id: int
    slug: str
    is_published: bool
    published_at: Optional[datetime] = None
    view_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class NewsListResponse(BaseModel):
    """Schema for paginated news list response."""
    items: List[NewsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class NewsPublishAction(BaseModel):
    """Schema for publish/unpublish action."""
    published_at: Optional[datetime] = None
