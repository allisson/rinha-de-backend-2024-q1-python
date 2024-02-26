from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="rinha_", env_file=".env", env_file_encoding="utf-8")
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    database_url: str
    database_pool_min_size: int = 5
    database_pool_max_size: int = 25


settings = Settings()
