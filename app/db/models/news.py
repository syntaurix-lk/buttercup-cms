"""
News/Blog Model
===============

Full CRUD model for managing news articles/blog posts.
Unlike CMS sections, news items are multiple rows requiring full CRUD operations.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Boolean, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class News(Base, TimestampMixin):
    """
    News/Blog article model.
    
    This model supports full CRUD operations:
    - Create: Add new news articles
    - Read: List/view articles (with filtering)
    - Update: Modify existing articles
    - Delete: Remove articles
    """
    __tablename__ = "news"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Basic info
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    slug: Mapped[str] = mapped_column(String(191), unique=True, nullable=False, index=True)
    
    # Content
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Media
    cover_image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Metadata
    author: Mapped[Optional[str]] = mapped_column(String(255), default="Admin")
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Comma-separated
    
    # Publishing
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # SEO
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Stats
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    
    def __repr__(self) -> str:
        return f"<News(id={self.id}, title='{self.title}', published={self.is_published})>"
