"""
Auth API Routes
===============

Simple admin login endpoints using HTTP Basic auth credentials.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.core.security import require_admin, verify_admin_plain
from app.core.logging import get_logger
from app.utils.api_response import success_response

router = APIRouter()
logger = get_logger(__name__)


class LoginRequest(BaseModel):
    """Login request payload."""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


@router.post("/login", response_model=dict, summary="Admin login")
def login(payload: LoginRequest):
    """Validate admin credentials and return a success response."""
    if verify_admin_plain(payload.username, payload.password):
        logger.info("Admin login success", extra={"username": payload.username})
        return success_response(
            data={"username": payload.username, "token_type": "basic"},
            message="Login successful",
        )

    logger.warning("Admin login failed", extra={"username": payload.username})
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


@router.get("/me", response_model=dict, summary="Get current admin")
def get_me(admin_user: str = Depends(require_admin)):
    """Return the authenticated admin username."""
    return success_response(data={"username": admin_user})


@router.post("/logout", response_model=dict, summary="Admin logout")
def logout():
    """No-op logout for Basic auth (client clears credentials)."""
    return success_response(message="Logged out")
