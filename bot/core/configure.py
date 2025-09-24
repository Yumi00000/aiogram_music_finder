from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)


class AcrCloudSettings(EnvBaseSettings):
    access_key: str
    access_secret: str
    host: str = "identify-eu-west-1.acrcloud.com"
    timeout: int = 10


class TelegramSettings(EnvBaseSettings):
    bot_token: str


class DB_Settings(EnvBaseSettings):
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int = 5432
    db_name: str
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"

class Settings(AcrCloudSettings, TelegramSettings, DB_Settings):
    debug: bool = True


settings = Settings()