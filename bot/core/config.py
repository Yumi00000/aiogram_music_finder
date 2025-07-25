from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

DIR = Path(__file__).absolute().parent.parent.parent
API_DIR = Path(__file__).absolute().parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)


class BotSettings(EnvBaseSettings):
    TELEGRAM_TOKEN: str
    ACRCLOUD_ACCESS_KEY: str
    ACRCLOUD_SECRET_KEY: str


class DBSettings(EnvBaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url(self) -> URL | str:
        if self.DB_PASS:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def local_database_url(self) -> URL | str:
        if self.DB_PASS:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@localhost:6432/{self.DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}@localhost:6432/{self.DB_NAME}"


class Settings(BotSettings, DBSettings):
    DEBUG: bool = True
    PROJECT_NAME: str = "Aiogram Music Finder"


settings = Settings()
