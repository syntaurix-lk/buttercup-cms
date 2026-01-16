"""
Assets Service
==============

Business logic for file/asset management.
"""

import logging
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.db.models.assets import Asset
from app.schemas.assets import AssetCreate, AssetUpdate
from app.utils.file_storage import file_storage
from app.core.config import settings

logger = logging.getLogger(__name__)


class AssetsService:
    """
    Service class for asset/file management.
    """
    
    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
    
    # =========================================================================
    # Upload Operations
    # =========================================================================
    
    async def upload_file(
        self,
        file: UploadFile,
        category: Optional[str] = None,
        alt_text: Optional[str] = None
    ) -> Asset:
        """
        Upload a file and create asset record.
        
        Args:
            file: The uploaded file
            category: Optional category for organization
            alt_text: Optional alt text for images
            
        Returns:
            Created asset record
        """
        # Save file to disk
        filename, file_path, file_size, width, height = await file_storage.save_file(file)
        
        # Create asset record
        asset = Asset(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            mime_type=file.content_type,
            file_size=file_size,
            width=width,
            height=height,
            category=category,
            alt_text=alt_text,
        )
        
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        
        logger.info(f"Uploaded asset: {asset.id} - {asset.filename}")
        return asset
    
    # =========================================================================
    # Read Operations
    # =========================================================================
    
    def get_by_id(self, asset_id: int) -> Optional[Asset]:
        """Get asset by ID."""
        return self.db.query(Asset).filter(Asset.id == asset_id).first()
    
    def get_by_filename(self, filename: str) -> Optional[Asset]:
        """Get asset by filename."""
        return self.db.query(Asset).filter(Asset.filename == filename).first()
    
    def get_by_path(self, file_path: str) -> Optional[Asset]:
        """Get asset by file path."""
        return self.db.query(Asset).filter(Asset.file_path == file_path).first()
    
    def list_assets(
        self,
        category: Optional[str] = None,
        is_active: Optional[bool] = True,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Asset], int]:
        """
        List assets with optional filtering.
        
        Args:
            category: Optional category filter
            is_active: Filter by active status
            page: Page number (1-indexed)
            page_size: Items per page
            
        Returns:
            Tuple of (assets list, total count)
        """
        query = self.db.query(Asset)
        
        if category:
            query = query.filter(Asset.category == category)
        
        if is_active is not None:
            query = query.filter(Asset.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        offset = (page - 1) * page_size
        assets = query.order_by(Asset.created_at.desc()).offset(offset).limit(page_size).all()
        
        return assets, total
    
    def get_categories(self) -> List[str]:
        """Get list of all unique categories."""
        result = self.db.query(Asset.category).filter(
            Asset.category.isnot(None),
            Asset.category != ""
        ).distinct().all()
        return [r[0] for r in result]
    
    # =========================================================================
    # Update Operations
    # =========================================================================
    
    def update(self, asset_id: int, data: AssetUpdate) -> Optional[Asset]:
        """
        Update asset metadata.
        
        Args:
            asset_id: ID of asset to update
            data: Update data
            
        Returns:
            Updated asset or None if not found
        """
        asset = self.get_by_id(asset_id)
        if not asset:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(asset, key, value)
        
        self.db.commit()
        self.db.refresh(asset)
        
        logger.info(f"Updated asset: {asset.id}")
        return asset
    
    # =========================================================================
    # Delete Operations
    # =========================================================================
    
    def delete(self, asset_id: int, delete_file: bool = True) -> bool:
        """
        Delete an asset and optionally its file.
        
        Args:
            asset_id: ID of asset to delete
            delete_file: Whether to delete the physical file
            
        Returns:
            True if deleted, False if not found
        """
        asset = self.get_by_id(asset_id)
        if not asset:
            return False
        
        # Delete physical file if requested
        if delete_file:
            file_storage.delete_file(asset.file_path)
        
        # Delete database record
        self.db.delete(asset)
        self.db.commit()
        
        logger.info(f"Deleted asset: {asset_id}")
        return True
    
    def delete_by_filename(self, filename: str, delete_file: bool = True) -> bool:
        """
        Delete an asset by filename.
        
        Args:
            filename: Filename of asset to delete
            delete_file: Whether to delete the physical file
            
        Returns:
            True if deleted, False if not found
        """
        asset = self.get_by_filename(filename)
        if not asset:
            return False
        
        return self.delete(asset.id, delete_file)
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    def get_file_url(self, asset: Asset) -> str:
        """Get the public URL for an asset."""
        return file_storage.get_file_url(asset.file_path)
    
    def to_response_dict(self, asset: Asset) -> dict:
        """Convert asset to response dictionary with URL."""
        return {
            "id": asset.id,
            "filename": asset.filename,
            "original_filename": asset.original_filename,
            "file_path": asset.file_path,
            "file_url": self.get_file_url(asset),
            "mime_type": asset.mime_type,
            "file_size": asset.file_size,
            "width": asset.width,
            "height": asset.height,
            "category": asset.category,
            "alt_text": asset.alt_text,
            "is_active": asset.is_active,
            "created_at": asset.created_at,
            "updated_at": asset.updated_at,
        }
