# app/settings.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bff_public_url:str = ""
    max_container_exec_time: int = 120
    tools_database_url:str = ""
    delete_container_after_ran:int = 0
    
    # docker_host: str
    redis_host: str
    redis_port: str
    
    class Config:
        env_file = ".env"

settings = Settings()
