"""
Core module containing configuration, logging, and DDL management.
"""

from app.core.config import settings
from app.core.logging import setup_logging, get_logger, set_request_id

__all__ = [
    "settings",
    "setup_logging",
    "get_logger",
    "set_request_id",
]
