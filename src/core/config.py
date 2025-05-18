from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    # CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"

settings = Settings()