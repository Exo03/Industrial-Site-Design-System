# server/db/migrations/env.py
import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import MetaData  # ← Используем отдельный MetaData!
from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

target_metadata = MetaData()

def run_migrations_offline():
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    from db.models.user import User
    from db.models.project import Project
    from db.models.element import Element
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
