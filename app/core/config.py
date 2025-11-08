from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Intelligent FAQ Bot"

    class Config:
        env_file = ".env"

settings = Settings()
