from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = Field(alias="LOG_LEVEL", default="INFO")
    MONGO_PORT: int = Field(alias="MONGO_PORT", default=123)
    MONGO_URI: str = Field(alias="MONGO_URI", default="url")
    MONGO_DB_NAME: str = Field(alias="MONGO_DB_NAME", default="name")
    MONGO_ROOT_USERNAME: str = Field(alias="MONGO_ROOT_USERNAME", default="user")
    MONGO_ROOT_PASSWORD: str = Field(alias="MONGO_ROOT_PASSWORD", default="pw")
    OPEN_AI_API_KEY: str = Field(alias="OPEN_AI_API_KEY", default="key")

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"


settings = Settings()
