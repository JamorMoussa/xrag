from botocore.config import Config as BotoConfig
from pathlib import PurePosixPath
import boto3

from .base import (
    StorageService, File, StorageKey, StorageType
)
from xrag.configs import Configs
from xrag.utils import get_object_key


class S3StorageService(StorageService):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__(configs=configs)
        
        self.client = boto3.client(
            "s3", 
            endpoint_url=self.configs.S3_ENDPOINT_URL,
            aws_access_key_id=self.configs.S3_ACCESS_KEY,
            aws_secret_access_key=self.configs.S3_SECRET_KEY,
            region_name=self.configs.S3_REGION,
            config= BotoConfig(
                signature_version=self.configs.S3_SIGNATURE_VERSION
            )
        )

    def upload(
        self, 
        file: File,
        storage_key: StorageKey
    ) -> str:

        name = None 

        if storage_key.storage_type is StorageType.RAW:
            name = storage_key.document_id
        else:
            name = storage_key.storage_type.value

        key = get_object_key(
            workspace_id=storage_key.workspace_id,
            document_id=storage_key.document_id,
            name=name,
            ext=storage_key.ext
        )

        extra_args = {}

        if content_type := storage_key.content_type:
            extra_args["ContentType"] = content_type

        self.client.upload_fileobj(
            Fileobj=file.content,
            Bucket=self.configs.S3_BUCKET,
            Key=key,
            ExtraArgs=extra_args or None,
        )

        return key

    def delete():
        pass

    def download(
        self, object_key: str
    ) -> File:

        response = self.client.get_object(
            Bucket=self.configs.S3_BUCKET,
            Key=object_key,
        )

        body = response["Body"]

        def chunks():
            try:
                yield from body.iter_chunks(chunk_size=64 * 1024)
            finally:
                body.close()

        return File(
            content=chunks(),
            filename=PurePosixPath(object_key).name,
            content_type=response.get("ContentType"),
        )