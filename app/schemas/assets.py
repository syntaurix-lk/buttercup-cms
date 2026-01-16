"""
Asset/Media Schemas
===================

Pydantic schemas for file/asset management.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    """Base asset schema."""
    category: Optional[str] = Field(default=None, max_length=100)
    alt_text: Optional[str] = Field(default=None, max_length=500)


class AssetCreate(AssetBase):
    """Schema for creating assets (used internally after file upload)."""
    filename: str
    original_filename: str
    file_path: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


class AssetUpdate(BaseModel):
    """Schema for updating asset metadata."""
    category: Optional[str] = Field(default=None, max_length=100)
    alt_text: Optional[str] = Field(default=None, max_length=500)
    is_active: Optional[bool] = None


class AssetResponse(BaseModel):
    """Schema for asset response."""
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_url: str  # Computed URL for frontend
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    category: Optional[str] = None
    alt_text: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class AssetListResponse(BaseModel):
    """Schema for asset list response."""
    items: List[AssetResponse]
    total: int


class AssetUploadResponse(BaseModel):
    """Schema for upload response."""
    asset: AssetResponse
    message: str = "File uploaded successfully"
