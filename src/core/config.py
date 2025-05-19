from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: str
    IS_TEST: int
    TEST_DB_NAME: str
    TEST_DB_HOST: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"

settings = Settings()