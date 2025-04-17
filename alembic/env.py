# alembic/env.py
import os
import sys
from logging.config import fileConfig
from typing import cast
from sqlalchemy import engine_from_config # Keep this
from sqlalchemy import pool # Keep this
from alembic import context

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from app.db.session import Base
from app.core.config import settings
from app.db.models import item as _
from app.db.models import user as _


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_sync_database_url() -> str:
    """Constructs the synchronous database URL for Alembic."""
    db_user = settings.DATABASE_USER
    db_password = settings.DATABASE_PASSWORD
    db_host = settings.DATABASE_HOST
    db_port = settings.DATABASE_PORT
    db_name = settings.DATABASE_NAME

    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_sync_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    main_section = config.get_main_option("config_main_section") or "alembic"
    alembic_config = cast(dict, config.get_section(main_section) or {})
    alembic_config["sqlalchemy.url"] = get_sync_database_url()
    connectable = engine_from_config(
        alembic_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
