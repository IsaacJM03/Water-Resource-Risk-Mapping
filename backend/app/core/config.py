from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Water Resource Risk Mapping"
    environment: str = "development"
    database_url: str = "mysql+pymysql://user:password@localhost:3306/water_risk"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
