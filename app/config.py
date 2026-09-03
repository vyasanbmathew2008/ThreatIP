from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    ip_api_url: str = "http://ip-api.com/json"

    class Config:
        env_file = ".env"


settings = Settings()
