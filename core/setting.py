from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_PORT: int
    MONGO_URI: str
    MONGO_DB_NAME: str
    MONGO_ROOT_USERNAME: str
    MONGO_ROOT_PASSWORD: str

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"


mongo_settings = Settings()
