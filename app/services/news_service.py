"""
News Service
============

Business logic for news/blog article management.
Supports full CRUD operations.
"""

import logging
from typing import Optional, List, Tuple
from datetime import datetime
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from slugify import slugify

from app.db.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate

logger = logging.getLogger(__name__)


class NewsService:
    """
    Service class for news article management.
    
    Provides full CRUD operations:
    - Create: Add new articles
    - Read: List and retrieve articles
    - Update: Modify existing articles
    - Delete: Remove articles
    """
    
    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    def _generate_unique_slug(self, title: str, exclude_id: Optional[int] = None) -> str:
        """
        Generate a unique slug from title.
        
        If slug already exists, appends a number suffix.
        """
        max_length = 191
        base_slug = slugify(title)[:max_length]
        slug = base_slug
        counter = 1
        
        while True:
            query = self.db.query(News).filter(News.slug == slug)
            if exclude_id:
                query = query.filter(News.id != exclude_id)
            
            if not query.first():
                return slug
            
            suffix = f"-{counter}"
            trimmed = base_slug[: max_length - len(suffix)]
            slug = f"{trimmed}{suffix}"
            counter += 1
    
    # =========================================================================
    # Create Operations
    # =========================================================================
    
    def create(self, data: NewsCreate) -> News:
        """
        Create a new news article.
        
        Args:
            data: News creation data
            
        Returns:
            Created news article
        """
        # Generate slug if not provided
        slug = data.slug if data.slug else self._generate_unique_slug(data.title)
        
        # Set published_at if publishing
        published_at = data.published_at
        if data.is_published and not published_at:
            published_at = datetime.utcnow()
        
        news = News(
            title=data.title,
            slug=slug,
            summary=data.summary,
            content=data.content,
            cover_image_path=data.cover_image_path,
            author=data.author,
            category=data.category,
            tags=data.tags,
            is_published=data.is_published,
            published_at=published_at,
            meta_title=data.meta_title,
            meta_description=data.meta_description,
        )
        
        self.db.add(news)
        self.db.commit()
        self.db.refresh(news)
        
        logger.info(f"Created news article: {news.id} - {news.title}")
        return news
    
    # =========================================================================
    # Read Operations
    # =========================================================================
    
    def get_by_id(self, news_id: int) -> Optional[News]:
        """Get news article by ID."""
        return self.db.query(News).filter(News.id == news_id).first()
    
    def get_by_slug(self, slug: str) -> Optional[News]:
        """Get news article by slug."""
        return self.db.query(News).filter(News.slug == slug).first()
    
    def list_published(
        self,
        page: int = 1,
        page_size: int = 10,
        category: Optional[str] = None
    ) -> Tuple[List[News], int]:
        """
        List published news articles for public view.
        
        Args:
            page: Page number (1-indexed)
            page_size: Items per page
            category: Optional category filter
            
        Returns:
            Tuple of (articles list, total count)
        """
        query = self.db.query(News).filter(News.is_published == True)
        
        if category:
            query = query.filter(News.category == category)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        offset = (page - 1) * page_size
        articles = query.order_by(desc(News.published_at)).offset(offset).limit(page_size).all()
        
        return articles, total
    
    def list_all(
        self,
        page: int = 1,
        page_size: int = 10,
        category: Optional[str] = None,
        is_published: Optional[bool] = None
    ) -> Tuple[List[News], int]:
        """
        List all news articles for admin view (includes drafts).
        
        Args:
            page: Page number (1-indexed)
            page_size: Items per page
            category: Optional category filter
            is_published: Optional published status filter
            
        Returns:
            Tuple of (articles list, total count)
        """
        query = self.db.query(News)
        
        if category:
            query = query.filter(News.category == category)
        
        if is_published is not None:
            query = query.filter(News.is_published == is_published)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        offset = (page - 1) * page_size
        articles = query.order_by(desc(News.created_at)).offset(offset).limit(page_size).all()
        
        return articles, total
    
    def get_categories(self) -> List[str]:
        """Get list of all unique categories."""
        result = self.db.query(News.category).filter(
            News.category.isnot(None),
            News.category != ""
        ).distinct().all()
        return [r[0] for r in result]
    
    # =========================================================================
    # Update Operations
    # =========================================================================
    
    def update(self, news_id: int, data: NewsUpdate) -> Optional[News]:
        """
        Update a news article.
        
        Args:
            news_id: ID of article to update
            data: Update data (partial update supported)
            
        Returns:
            Updated article or None if not found
        """
        news = self.get_by_id(news_id)
        if not news:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        
        # Handle slug update
        if "slug" in update_data and update_data["slug"]:
            update_data["slug"] = self._generate_unique_slug(update_data["slug"], news_id)
        elif "title" in update_data and not data.slug:
            # Regenerate slug if title changed but no slug provided
            update_data["slug"] = self._generate_unique_slug(update_data["title"], news_id)
        
        # Handle published_at
        if "is_published" in update_data:
            if update_data["is_published"] and not news.published_at:
                update_data["published_at"] = datetime.utcnow()
        
        # Apply updates
        for key, value in update_data.items():
            setattr(news, key, value)
        
        self.db.commit()
        self.db.refresh(news)
        
        logger.info(f"Updated news article: {news.id}")
        return news
    
    def publish(self, news_id: int, published_at: Optional[datetime] = None) -> Optional[News]:
        """
        Publish a news article.
        
        Args:
            news_id: ID of article to publish
            published_at: Optional specific publish date
            
        Returns:
            Published article or None if not found
        """
        news = self.get_by_id(news_id)
        if not news:
            return None
        
        news.is_published = True
        news.published_at = published_at or datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(news)
        
        logger.info(f"Published news article: {news.id}")
        return news
    
    def unpublish(self, news_id: int) -> Optional[News]:
        """
        Unpublish a news article.
        
        Args:
            news_id: ID of article to unpublish
            
        Returns:
            Unpublished article or None if not found
        """
        news = self.get_by_id(news_id)
        if not news:
            return None
        
        news.is_published = False
        
        self.db.commit()
        self.db.refresh(news)
        
        logger.info(f"Unpublished news article: {news.id}")
        return news
    
    def increment_view_count(self, news_id: int) -> None:
        """Increment view count for an article."""
        self.db.query(News).filter(News.id == news_id).update(
            {News.view_count: News.view_count + 1}
        )
        self.db.commit()
    
    # =========================================================================
    # Delete Operations
    # =========================================================================
    
    def delete(self, news_id: int) -> bool:
        """
        Delete a news article.
        
        Args:
            news_id: ID of article to delete
            
        Returns:
            True if deleted, False if not found
        """
        news = self.get_by_id(news_id)
        if not news:
            return False
        
        self.db.delete(news)
        self.db.commit()
        
        logger.info(f"Deleted news article: {news_id}")
        return True
