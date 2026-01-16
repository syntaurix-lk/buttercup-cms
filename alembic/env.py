"""
Alembic Migration Environment
=============================

This file configures Alembic to work with our SQLAlchemy models
and load database configuration from the application settings.
"""

import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our models and config
from app.core.config import settings
from app.db.base import Base

# Import all models to ensure they're registered with Base.metadata
from app.db.models import cms, news, assets  # noqa: F401

# This is the Alembic Config object
config = context.config

# Override sqlalchemy.url with our settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    allowing SQL to be generated without a DB connection.
    
    Calls to context.execute() emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Include object names in autogenerate comparisons
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Enable comparison of column types
            compare_type=True,
            # Enable comparison of server defaults
            compare_server_default=True,
            # Render item names with schema info
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Run either offline or online based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
