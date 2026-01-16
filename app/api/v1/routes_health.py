"""
Health Check Routes
===================

Provides health check endpoints for monitoring API and database status.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.db.session import get_db
from app.utils.api_response import api_response
from app.core.config import settings
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check endpoint.
    
    Returns:
    - API status
    - Database connectivity
    - Configuration summary
    - Timestamp
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": settings.APP_ENV,
        "components": {
            "api": {"status": "up"},
            "database": {"status": "unknown"}
        }
    }
    
    # Check database connectivity
    try:
        db.execute(text("SELECT 1"))
        health_status["components"]["database"] = {
            "status": "up",
            "type": "MySQL"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["status"] = "degraded"
        health_status["components"]["database"] = {
            "status": "down",
            "error": str(e) if settings.DEBUG else "Connection failed"
        }
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    
    return api_response(
        success=health_status["status"] == "healthy",
        message=f"Service is {health_status['status']}",
        data=health_status
    )


@router.get("/health/live")
async def liveness_probe():
    """
    Kubernetes-style liveness probe.
    Returns 200 if the application is running.
    """
    return api_response(
        success=True,
        message="Service is alive",
        data={"status": "alive", "timestamp": datetime.utcnow().isoformat()}
    )


@router.get("/health/ready")
async def readiness_probe(db: Session = Depends(get_db)):
    """
    Kubernetes-style readiness probe.
    Returns 200 if the application is ready to accept traffic.
    """
    try:
        db.execute(text("SELECT 1"))
        return api_response(
            success=True,
            message="Service is ready",
            data={"status": "ready", "timestamp": datetime.utcnow().isoformat()}
        )
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return api_response(
            success=False,
            message="Service is not ready",
            errors=[str(e) if settings.DEBUG else "Database not available"]
        )
