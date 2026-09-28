from botocore.config import Config as BotoConfig
from pathlib import PurePosixPath
from io import BytesIO
import boto3
import asyncio

from .base import StorageService, File
from xrag.configs import Configs


class S3StorageService(StorageService):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__(configs=configs)

        self.bucket = self.configs.S3_BUCKET
        
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

    async def upload(
        self,
        object_key,
        fileobj: BytesIO,
        content_type: str | None = None
    ):
        extra_args = {}

        if content_type:
            extra_args["ContentType"] = content_type

        self.client.upload_fileobj(
            Fileobj=fileobj,
            Bucket=self.bucket,
            Key=object_key,
            ExtraArgs=extra_args or None,
        )

    async def delete(
        self, 
        object_key
    ):
        self.client.delete_object(
            Bucket=self.bucket,
            Key=object_key,
        )

    async def download(
        self, object_key: str
    ) -> File:

        response = await asyncio.to_thread(
            self.client.get_object,
            Bucket=self.bucket,
            Key=object_key,
        )

        body = response["Body"]
        try:
            content = await asyncio.to_thread(body.read)
        finally:
            body.close()

        return File(
            content=content,
            filename=PurePosixPath(object_key).name,
            content_type=response.get("ContentType"),
        )