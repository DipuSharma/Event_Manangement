import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TITLE = os.getenv("TITLE")
    DEBUG = os.getenv("DEBUG")
    ALGORITHM = os.getenv("ALGO")
    HOST_URL = os.getenv("HOST_URL")
    HOST_PORT = os.getenv("HOST_PORT")
    SECRET_KEY = os.getenv("SECRET_KEY")
    POSTGRES_SQL = os.getenv("DATABASE_URL")
    BASE_DIR = Path(__file__).resolve().parent
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


setting = Settings()
