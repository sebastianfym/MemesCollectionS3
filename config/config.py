from pydantic.v1 import BaseSettings

import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


class Settings(BaseSettings):
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    S3_ENDPOINT_URL: str = S3_ENDPOINT_URL
    S3_ACCESS_KEY: str = S3_ACCESS_KEY
    S3_SECRET_KEY: str = S3_SECRET_KEY
    S3_BUCKET_NAME: str = S3_BUCKET_NAME



settings = Settings()
