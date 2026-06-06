from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    enviornment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()