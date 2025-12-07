
# server/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Базовые настройки
    APP_NAME: str = "Industrial-Site-Design-System"
    DEBUG: bool = False
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # БД
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = 'J73ZyKfifH8x1AB4kYuNWvrQ9K6OA5VZ'
    POSTGRES_HOST: str = "dpg-d4iurf15pdvs7385ojl0-a"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "industrial_site_design_system"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
