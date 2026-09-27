from pydantic_settings import BaseSettings, SettingsConfigDict

API_PREFIX_PATH = "/api/v1"

class Configs(BaseSettings):

    APP_NAME: str
    API_VERSION: str

    #---- S3 Configs: 
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str
    S3_BUCKET: str
    S3_SIGNATURE_VERSION: str

    #---- File type
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


def get_configs() -> Configs:
    return Configs()