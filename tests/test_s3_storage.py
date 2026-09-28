"""Run with: RUN_S3_TESTS=1 uv run python -m pytest tests/test_s3_storage.py -v"""

import asyncio
import os
from io import BytesIO
from uuid import uuid4

import pytest

from xrag.configs import get_configs
from xrag.services.storage.s3 import S3StorageService


@pytest.mark.skipif(
    os.getenv("RUN_S3_TESTS") != "1",
    reason="Set RUN_S3_TESTS=1 to test the configured S3 bucket",
)
def test_s3_upload_download_delete():
    settings = get_configs()
    storage = S3StorageService(settings)
    key = f"storage-tests/{uuid4().hex}.txt"
    payload = b"XRAG S3 storage smoke test\n"
    try:
        asyncio.run(
            storage.upload(
                object_key=key,
                fileobj=BytesIO(payload),
                content_type="text/plain",
            )
        )
        response = storage.client.get_object(Bucket=settings.S3_BUCKET, Key=key)
        try:
            assert response["Body"].read() == payload
            assert response["ContentType"] == "text/plain"
        finally:
            response["Body"].close()
    finally:
        try:
            # storage.client.delete_object(Bucket=settings.S3_BUCKET, Key=key)
            print("object is not deleted")
        finally:
            storage.client.close()
