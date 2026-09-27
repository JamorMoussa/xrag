from pydantic_settings import BaseSettings, SettingsConfigDict

API_PREFIX_PATH = "/api/v1"

class Configs(BaseSettings):

    app_name: str
    api_version: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


def get_configs() -> Configs:
    return Configs()