"""
Logging Configuration
=====================

IMPORTANT: log4j2 is a Java-only logging framework and cannot be used in Python.

This module implements Python's best practice logging with features equivalent to log4j2:
- Console logging with colored output
- Rotating file logs (similar to log4j2's RollingFileAppender)
- Structured JSON logs (similar to log4j2's JSONLayout)
- Request-ID correlation (similar to log4j2's MDC/ThreadContext)
- Never logs secrets or sensitive data

Features:
- Console + File handlers with configurable levels
- Automatic log rotation by size (RollingFileAppender equivalent)
- JSON structured logging for production (JSONLayout equivalent)
- Request ID correlation via contextvars (MDC equivalent)
- Filters to prevent logging of sensitive data
"""

import logging
import sys
import os
import re
from logging.handlers import RotatingFileHandler
from contextvars import ContextVar
from typing import Optional
from datetime import datetime
from pythonjsonlogger import jsonlogger

from app.core.config import settings

# ContextVar for request ID correlation (similar to log4j2's MDC)
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    """
    Filter that adds request_id to log records.
    Similar to log4j2's MDC (Mapped Diagnostic Context).
    """
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get() or "N/A"
        return True


class SensitiveDataFilter(logging.Filter):
    """
    Filter to mask sensitive data in logs.
    Never log passwords, tokens, or secrets.
    """
    
    SENSITIVE_PATTERNS = [
        (re.compile(r'password["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', re.I), r'password=***REDACTED***'),
        (re.compile(r'token["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', re.I), r'token=***REDACTED***'),
        (re.compile(r'secret["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', re.I), r'secret=***REDACTED***'),
        (re.compile(r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', re.I), r'api_key=***REDACTED***'),
        (re.compile(r'authorization["\']?\s*[:=]\s*["\']?([^"\'\s,}]+)', re.I), r'authorization=***REDACTED***'),
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        if record.msg:
            msg = str(record.msg)
            for pattern, replacement in self.SENSITIVE_PATTERNS:
                msg = pattern.sub(replacement, msg)
            record.msg = msg
        return True


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter for structured logging.
    Similar to log4j2's JSONLayout.
    """
    
    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super().add_fields(log_record, record, message_dict)
        
        # Add timestamp in ISO format
        log_record["timestamp"] = datetime.utcnow().isoformat() + "Z"
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["request_id"] = getattr(record, "request_id", "N/A")
        
        # Add location info
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno
        
        # Add environment
        log_record["environment"] = settings.APP_ENV
        log_record["service"] = settings.APP_NAME


class ColoredFormatter(logging.Formatter):
    """
    Colored formatter for console output in development.
    """
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging() -> logging.Logger:
    """
    Setup application logging.
    
    Returns:
        Configured root logger
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(settings.LOG_FILE_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Add filters
    request_id_filter = RequestIdFilter()
    sensitive_filter = SensitiveDataFilter()
    
    # =========================================================================
    # Console Handler
    # =========================================================================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    console_handler.addFilter(request_id_filter)
    console_handler.addFilter(sensitive_filter)
    
    if settings.LOG_FORMAT == "json":
        console_formatter = CustomJsonFormatter()
    else:
        # Text format with colors for development
        console_formatter = ColoredFormatter(
            "%(asctime)s | %(levelname)s | [%(request_id)s] | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # =========================================================================
    # File Handler (Rotating - similar to log4j2's RollingFileAppender)
    # =========================================================================
    file_handler = RotatingFileHandler(
        settings.LOG_FILE_PATH,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    file_handler.addFilter(request_id_filter)
    file_handler.addFilter(sensitive_filter)
    
    # Always use JSON format for file logs (easier to parse in production)
    file_formatter = CustomJsonFormatter()
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger with proper configuration.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger
    """
    return logging.getLogger(name)


def set_request_id(request_id: str) -> None:
    """
    Set the request ID for the current context.
    Similar to log4j2's MDC.put() method.
    
    Args:
        request_id: Unique identifier for the current request
    """
    request_id_var.set(request_id)


def get_request_id() -> Optional[str]:
    """
    Get the current request ID from context.
    Similar to log4j2's MDC.get() method.
    
    Returns:
        Current request ID or None
    """
    return request_id_var.get()
