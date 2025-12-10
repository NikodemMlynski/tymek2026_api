from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_url: str 
    admin_code: str
    model_config = ConfigDict(env_file=".env")

settings = Settings()