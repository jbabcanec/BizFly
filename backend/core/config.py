from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "BizFly"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    database_url: str = Field(
        default="postgresql://bizfly:bizfly@localhost:5432/bizfly",
        env="DATABASE_URL"
    )
    
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    google_maps_api_key: str = Field(default="", env="GOOGLE_MAPS_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="JWT_SECRET_KEY"
    )
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        env="CORS_ORIGINS"
    )
    
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()