"""
Assets API Routes
=================

Endpoints for file/image upload and management.

- POST /assets/upload - Upload a file
- GET /assets - List assets
- GET /assets/{asset_id} - Get asset details
- PATCH /assets/{asset_id} - Update asset metadata
- DELETE /assets/{asset_id} - Delete asset
- DELETE /assets/filename/{filename} - Delete asset by filename
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.assets_service import AssetsService
from app.utils.api_response import success_response

router = APIRouter()


def get_assets_service(db: Session = Depends(get_db)) -> AssetsService:
    """Dependency to get assets service instance."""
    return AssetsService(db)


@router.post("/upload", response_model=dict, summary="Upload file")
async def upload_file(
    file: UploadFile = File(..., description="File to upload"),
    category: Optional[str] = Form(None, description="Category for organization"),
    alt_text: Optional[str] = Form(None, description="Alt text for images"),
    service: AssetsService = Depends(get_assets_service)
):
    """
    Upload a file (image).
    
    - Validates file type (only allowed image types)
    - Limits file size (configurable via env)
    - Saves file to uploads directory
    - Returns asset details with public URL
    """
    asset = await service.upload_file(file, category, alt_text)
    
    return success_response(
        data=service.to_response_dict(asset),
        message="File uploaded successfully"
    )


@router.get("", response_model=dict, summary="List assets")
def list_assets(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    service: AssetsService = Depends(get_assets_service)
):
    """List uploaded assets with optional filtering."""
    assets, total = service.list_assets(category, is_active, page, page_size)
    
    return success_response(
        data={
            "items": [service.to_response_dict(a) for a in assets],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/categories", response_model=dict, summary="List asset categories")
def list_categories(service: AssetsService = Depends(get_assets_service)):
    """Get list of all asset categories."""
    categories = service.get_categories()
    return success_response(data=categories)


@router.get("/{asset_id}", response_model=dict, summary="Get asset details")
def get_asset(
    asset_id: int,
    service: AssetsService = Depends(get_assets_service)
):
    """Get asset details by ID."""
    asset = service.get_by_id(asset_id)
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return success_response(data=service.to_response_dict(asset))


@router.patch("/{asset_id}", response_model=dict, summary="Update asset metadata")
def update_asset(
    asset_id: int,
    category: Optional[str] = Form(None),
    alt_text: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    service: AssetsService = Depends(get_assets_service)
):
    """Update asset metadata."""
    from app.schemas.assets import AssetUpdate
    
    update_data = AssetUpdate(
        category=category,
        alt_text=alt_text,
        is_active=is_active
    )
    
    asset = service.update(asset_id, update_data)
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return success_response(
        data=service.to_response_dict(asset),
        message="Asset updated successfully"
    )


@router.delete("/{asset_id}", response_model=dict, summary="Delete asset by ID")
def delete_asset(
    asset_id: int,
    delete_file: bool = Query(True, description="Also delete physical file"),
    service: AssetsService = Depends(get_assets_service)
):
    """Delete an asset by ID."""
    deleted = service.delete(asset_id, delete_file)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return success_response(message="Asset deleted successfully")


@router.delete("/filename/{filename}", response_model=dict, summary="Delete asset by filename")
def delete_asset_by_filename(
    filename: str,
    delete_file: bool = Query(True, description="Also delete physical file"),
    service: AssetsService = Depends(get_assets_service)
):
    """Delete an asset by filename."""
    deleted = service.delete_by_filename(filename, delete_file)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return success_response(message="Asset deleted successfully")
