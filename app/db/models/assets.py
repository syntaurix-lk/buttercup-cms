"""
Asset/Media Model
=================

Model for tracking uploaded files/images.
"""

from typing import Optional
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Asset(Base, TimestampMixin):
    """
    Asset/Media file tracking model.
    
    Tracks all uploaded files for management and reference.
    """
    __tablename__ = "assets"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # File information
    filename: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(191), nullable=False, unique=True)
    
    # File metadata
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # In bytes
    
    # Image dimensions (if applicable)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Organization
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    alt_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    def __repr__(self) -> str:
        return f"<Asset(id={self.id}, filename='{self.filename}')>"
