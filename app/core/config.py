from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Intelligent FAQ Bot"
    SAVE_THRESHOLD: int = 3

    class Config:
        env_file = ".env"

settings = Settings()
