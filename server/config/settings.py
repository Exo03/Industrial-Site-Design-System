
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
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = 'DPwFoJyRoiopsUTaTtonokmRuYmkOULL'
    POSTGRES_HOST: str = "mainline.proxy.rlwy.net"
    POSTGRES_PORT: int = 42637
    POSTGRES_DB: str = "railway"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
