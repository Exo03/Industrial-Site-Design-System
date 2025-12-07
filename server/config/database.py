# server/config/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from server.config.settings import settings

# Асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG, 
    future=True,
)

# Фабрика сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency для FastAPI: получение сессии
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:

            await session.close()

