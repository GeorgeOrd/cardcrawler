from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings (BaseSettings):
    app_name: str = "Card Crawler API"
    max_attemps: int = 3
    api_prefix: str = "/api/v1"
    SCG_URL: str
    ALLOW_ORIGINS: str
    model_config = SettingsConfigDict(env_file=".env")
        
settings = Settings()