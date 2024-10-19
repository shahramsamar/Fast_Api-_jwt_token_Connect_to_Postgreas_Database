
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:0000@127.0.0.1:5432/blog"

    
    SECRET_KEY: str = "change me"
    ACCESS_EXPIRATION: int = 60  # 1 hour
    REFRESH_EXPIRATION: int = 10080  # 7 days


settings = Settings()
