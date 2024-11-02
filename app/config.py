import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "123456789")
    ALGORITHM: str = os.getenv("HASH_ALGORITHM", "HS512")


settings = Settings()
