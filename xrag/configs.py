from pydantic_settings import BaseSettings, SettingsConfigDict

class Configs(BaseSettings):

    API_PREFIX_PATH: str 
    API_NAME: str
    API_VERSION: str

    #--- Services:
    STORAGE_BASE_URL: str 
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str
    S3_BUCKET: str
    S3_SIGNATURE_VERSION: str


    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int 

    LITE_PARSER_BASE_URL: str

    # ---- Temporal
    TEMPORAL_HOST: str
    TEMPORAL_NAMESPACE: str
    TEMPORAL_TASK_QUEUE: str

    # ----- Ollama
    EMBEDDING_PROVIDER: str
    EMBEDDING_MODEL: str
    EMBEDDING_BASE_URL: str

    # ----- VecDB
    VECDB_PROVIDER: str
    VECDB_BASE_URL: str
    VECDB_COLLECTION: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


def get_configs() -> Configs:
    return Configs()

configs = Configs()