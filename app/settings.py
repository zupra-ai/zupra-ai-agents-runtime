# app/settings.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    docker_host: str
    redis_host: str
    redis_port: str

    class Config:
        env_file = ".env"


settings = Settings()
