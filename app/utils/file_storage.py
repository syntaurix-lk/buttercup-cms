"""
File Storage Utility
====================

Handles file uploads with validation:
- Validates file types (only allowed image types)
- Limits file sizes (configurable via env)
- Saves files to the upload directory
- Returns public URLs for accessing files
- Images are stored as FILES, not base64
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path

from fastapi import UploadFile, HTTPException
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)


class FileStorage:
    """
    File storage handler for managing uploads.
    """
    
    def __init__(self):
        """Initialize storage with configured upload directory."""
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self._ensure_upload_dir()
    
    def _ensure_upload_dir(self):
        """Create upload directory if it doesn't exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Upload directory ensured: {self.upload_dir}")
    
    def validate_file(self, file: UploadFile) -> None:
        """
        Validate uploaded file.
        
        Args:
            file: The uploaded file to validate
            
        Raises:
            HTTPException: If validation fails
        """
        # Check if file is provided
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check content type
        content_type = file.content_type or ""
        if content_type not in settings.allowed_image_types_list:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {content_type}. Allowed types: {settings.ALLOWED_IMAGE_TYPES}"
            )
        
        logger.debug(f"File validated: {file.filename}, type: {content_type}")
    
    async def validate_file_size(self, file: UploadFile) -> int:
        """
        Validate file size.
        
        Args:
            file: The uploaded file
            
        Returns:
            File size in bytes
            
        Raises:
            HTTPException: If file is too large
        """
        # Read file content to check size
        content = await file.read()
        file_size = len(content)
        
        # Reset file position for later reading
        await file.seek(0)
        
        if file_size > settings.max_upload_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_MB}MB"
            )
        
        logger.debug(f"File size validated: {file_size} bytes")
        return file_size
    
    def generate_filename(self, original_filename: str) -> str:
        """
        Generate a unique filename to prevent collisions.
        
        Args:
            original_filename: The original filename
            
        Returns:
            Unique filename with timestamp and UUID
        """
        # Get file extension
        ext = Path(original_filename).suffix.lower()
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        
        return f"{timestamp}_{unique_id}{ext}"
    
    async def save_file(
        self,
        file: UploadFile,
        subfolder: Optional[str] = None
    ) -> Tuple[str, str, int, Optional[int], Optional[int]]:
        """
        Save uploaded file to disk.
        
        Args:
            file: The uploaded file
            subfolder: Optional subfolder within upload directory
            
        Returns:
            Tuple of (filename, file_path, file_size, width, height)
            width and height are only for images
        """
        # Validate file
        self.validate_file(file)
        file_size = await self.validate_file_size(file)
        
        # Generate unique filename
        filename = self.generate_filename(file.filename)
        
        # Determine save path
        if subfolder:
            save_dir = self.upload_dir / subfolder
            save_dir.mkdir(parents=True, exist_ok=True)
            file_path = f"{subfolder}/{filename}"
        else:
            save_dir = self.upload_dir
            file_path = filename
        
        full_path = save_dir / filename
        
        # Read file content
        content = await file.read()
        
        # Save file
        with open(full_path, "wb") as f:
            f.write(content)
        
        logger.info(f"File saved: {full_path}")
        
        # Get image dimensions if it's an image
        width, height = None, None
        try:
            if file.content_type and file.content_type.startswith("image/") and file.content_type != "image/svg+xml":
                with Image.open(full_path) as img:
                    width, height = img.size
        except Exception as e:
            logger.warning(f"Could not get image dimensions: {e}")
        
        return filename, file_path, file_size, width, height
    
    def get_file_url(self, file_path: str) -> str:
        """
        Get the public URL for a file.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            Public URL to access the file
        """
        return f"{settings.STATIC_URL_PREFIX}/{settings.UPLOAD_DIR}/{file_path}"
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            True if deleted, False if not found
        """
        full_path = self.upload_dir / file_path
        
        if full_path.exists():
            full_path.unlink()
            logger.info(f"File deleted: {full_path}")
            return True
        
        logger.warning(f"File not found for deletion: {full_path}")
        return False
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            True if exists, False otherwise
        """
        return (self.upload_dir / file_path).exists()


# Global storage instance
file_storage = FileStorage()
