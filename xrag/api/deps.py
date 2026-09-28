from fastapi import Depends
from typing import Annotated

from xrag.configs import get_configs, Configs
from xrag.services.storage.s3 import S3StorageService
from xrag.services.ingest.parse import LiteParserService


def get_storage_service(
    configs: Annotated[Configs, Depends(get_configs)]
) -> S3StorageService:
    return S3StorageService(configs=configs)


def get_liteparser_service(
    configs: Annotated[Configs, Depends(get_configs)]
) -> LiteParserService:
    return LiteParserService(configs=configs)