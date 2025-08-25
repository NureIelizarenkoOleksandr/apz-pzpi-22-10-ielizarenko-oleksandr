import os
from pydantic_settings import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# dotenv_path = BASE_DIR / ".env"
# load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):
    SECRET_KEY: str = "test"
    ADMIN_USERNAME: str = "test"
    ADMIN_PASSWORD: str = "test"

    POSTGRES_USER: str = "test"
    POSTGRES_PASSWORD: str = "test"
    POSTGRES_HOST: str = "test"
    POSTGRES_PORT: str = "test"
    POSTGRES_DB: str = "test"

    @property
    def sqlalchemy_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def sqlalchemy_sync_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()