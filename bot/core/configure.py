from pathlib import Path
from typing import ClassVar
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class EnvBaseSettings(BaseSettings):
    pass


class AcrCloudSettings(EnvBaseSettings):
    ACRCLOUD_ACCESS_KEY: str
    ACRCLOUD_SECRET_KEY: str
    acr_host: str = "identify-eu-west-1.acrcloud.com"
    acr_timeout: int = 10


class TelegramSettings(EnvBaseSettings):
    TELEGRAM_TOKEN: str


class DB_Settings(EnvBaseSettings):
    DB_USER: str
    DB_PASS: SecretStr
    DB_HOST: str
    db_port: int = 5432
    DB_NAME: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS.get_secret_value()}@{self.DB_HOST}:{self.db_port}/{self.DB_NAME}"


class Settings(AcrCloudSettings, TelegramSettings, DB_Settings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
    DEBUG: bool = True
    PROJECT_ROOT: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent
    DOWNLOADS_DIR: ClassVar[Path] = PROJECT_ROOT / "bot" / "downloads"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
