"""
Standard API Response Format
============================

All API endpoints should return responses in this consistent format:
{
    "success": true/false,
    "message": "Human-readable message",
    "data": {...} or [...] or null,
    "errors": [...] or null
}
"""

from typing import Any, Optional, List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper.
    
    Attributes:
        success: Whether the operation was successful
        message: Human-readable message about the operation
        data: The actual response data (can be any type)
        errors: List of error details (if any)
    """
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[List[str]] = None
    
    model_config = {"from_attributes": True}


def success_response(
    data: Any = None,
    message: str = "Operation successful"
) -> dict:
    """
    Create a standardized success response.
    
    Args:
        data: The response payload
        message: Success message
        
    Returns:
        Dictionary in the standard response format
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": None
    }


def error_response(
    message: str = "Operation failed",
    errors: Optional[List[str]] = None
) -> dict:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        errors: List of specific error details
        
    Returns:
        Dictionary in the standard response format
    """
    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors or []
    }


def api_response(
    success: bool = True,
    message: str = "Operation successful",
    data: Any = None,
    errors: Optional[List[str]] = None
) -> dict:
    """
    Create a standardized API response.
    
    This is the main function used throughout the application
    for consistent response formatting.
    
    Args:
        success: Whether the operation was successful
        message: Human-readable message
        data: The response payload
        errors: List of error details (if any)
        
    Returns:
        Dictionary in the standard response format
    
    Examples:
        >>> api_response(success=True, message="User created", data={"id": 1})
        {"success": True, "message": "User created", "data": {"id": 1}, "errors": None}
        
        >>> api_response(success=False, message="Validation failed", errors=["Invalid email"])
        {"success": False, "message": "Validation failed", "data": None, "errors": ["Invalid email"]}
    """
    return {
        "success": success,
        "message": message,
        "data": data,
        "errors": errors
    }
