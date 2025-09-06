from alembic import context
from sqlalchemy import engine_from_config, pool

# 1) Import your metadata (tables) and settings
from app.db.base import Base                  # Declarative Base
from app.models import models                 # ensure models are imported so metadata is populated
from app.core.config import get_settings

settings = get_settings()

# 2) Tell Alembic which DB URL to use (from .env)
config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

# 3) Point Alembic at your metadata (tables)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.database_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
