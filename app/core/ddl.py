"""
DDL Auto Management
===================

This module implements Spring Boot-like ddl-auto behavior using Alembic migrations.

Configuration (via DB_DDL_AUTO environment variable):
-----------------------------------------------------
- create: Drop ALL tables and recreate schema from scratch
          WARNING: This DELETES ALL DATA! Use only in development.
          
- update: Run Alembic migrations to apply incremental changes safely.
          This is the RECOMMENDED mode for production.
          
- none:   Do nothing on startup. Manual migration control.

How it works:
-------------
1. "create" mode:
   - Drops all tables using SQLAlchemy metadata
   - Creates all tables fresh using Base.metadata.create_all()
   - DANGER: All data will be lost!
   
2. "update" mode:
   - Runs `alembic upgrade head` programmatically
   - Applies only pending migrations
   - Safe for production use
   
3. "none" mode:
   - Skips all DDL operations
   - You must run migrations manually: `alembic upgrade head`

Why use Alembic for "update"?
-----------------------------
SQLAlchemy's create_all() only creates missing tables - it cannot:
- Add columns to existing tables
- Modify column types
- Add/remove indexes
- Handle complex schema changes

Alembic migrations provide:
- Version-controlled schema changes
- Rollback capability
- Data migrations
- Safe production deployments
"""

import logging
from sqlalchemy import text
from alembic.config import Config
from alembic import command

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

logger = logging.getLogger(__name__)


def run_ddl_auto():
    """
    Execute DDL auto behavior based on configuration.
    
    This should be called on application startup.
    """
    ddl_mode = settings.DB_DDL_AUTO
    logger.info(f"DDL Auto Mode: {ddl_mode}")
    
    if ddl_mode == "create":
        _handle_create_mode()
    elif ddl_mode == "update":
        _handle_update_mode()
    elif ddl_mode == "none":
        logger.info("DDL Auto: 'none' - Skipping all DDL operations")
    else:
        logger.warning(f"Unknown DDL_AUTO mode: {ddl_mode}. Skipping DDL operations.")


def _handle_create_mode():
    """
    Handle 'create' mode - drop and recreate all tables.
    
    WARNING: This will DELETE ALL DATA!
    """
    if settings.APP_ENV == "prod":
        logger.error("DANGER: DB_DDL_AUTO=create is not allowed in production!")
        logger.error("Please use 'update' or 'none' mode in production.")
        raise RuntimeError("Cannot use 'create' mode in production environment")
    
    logger.warning("=" * 60)
    logger.warning("DDL Auto: 'create' mode - DROPPING ALL TABLES!")
    logger.warning("This will DELETE ALL DATA in the database!")
    logger.warning("=" * 60)
    
    # Import all models to ensure they're registered with Base
    _import_all_models()
    
    # Drop all tables
    logger.info("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("DDL Auto: 'create' completed successfully")


def _handle_update_mode():
    """
    Handle 'update' mode - run Alembic migrations.
    
    This is the recommended mode for production.
    """
    logger.info("DDL Auto: 'update' mode - Running Alembic migrations...")
    
    try:
        # Create Alembic config
        alembic_cfg = Config("alembic.ini")
        
        # Run migrations to head
        command.upgrade(alembic_cfg, "head")
        
        logger.info("DDL Auto: Migrations completed successfully")
    except Exception as e:
        logger.error(f"DDL Auto: Migration failed - {str(e)}")
        logger.warning("If this is a fresh database, try running: alembic upgrade head")
        raise


def _import_all_models():
    """
    Import all models to ensure they're registered with SQLAlchemy Base.
    
    This is necessary for create_all() to know about all tables.
    """
    # Import models - this registers them with Base.metadata
    from app.db.models import cms, news, assets  # noqa: F401
    logger.debug("All models imported successfully")


def check_database_connection():
    """
    Check if database connection is working.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False


async def handle_ddl_auto(engine_instance, ddl_mode: str):
    """
    Async wrapper for DDL auto behavior.
    
    Called from FastAPI lifespan handler.
    
    Args:
        engine_instance: SQLAlchemy engine instance
        ddl_mode: DDL mode (create/update/none)
    """
    run_ddl_auto()
