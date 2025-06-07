import os
from pydantic_settings import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):
    SECRET_KEY: str

settings = Settings()