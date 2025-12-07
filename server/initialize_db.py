import asyncio
import os
from server.db.migrations.alembic import command
from server.db.migrations.alembic.config import Config

async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    asyncio.run(run_migrations())
