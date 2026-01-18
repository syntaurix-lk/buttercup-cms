"""
Admin Authentication Helpers
============================

Provides HTTP Basic auth for admin-only endpoints.
"""

import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
security = HTTPBasic()


def _credentials_match(username: str, password: str) -> bool:
    """Constant-time check for admin credentials."""
    if not username or not password:
        return False
    return (
        secrets.compare_digest(username, settings.ADMIN_USERNAME)
        and secrets.compare_digest(password, settings.ADMIN_PASSWORD)
    )


def verify_admin_plain(username: str, password: str) -> bool:
    """Verify admin credentials from a plain payload."""
    return _credentials_match(username, password)


def require_admin(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Dependency that enforces admin authentication.

    Returns:
        The authenticated username.
    """
    if not _credentials_match(credentials.username, credentials.password):
        logger.warning("Admin auth failed", extra={"username": credentials.username})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    logger.debug("Admin auth ok", extra={"username": credentials.username})
    return credentials.username
