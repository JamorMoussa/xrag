from fastapi import APIRouter, Depends, UploadFile
from pathlib import Path
from typing import Annotated

from xrag.configs import API_PREFIX_PATH
from ..deps import get_storage_service
from xrag.services.ingest.upload import UploadService
from xrag.services.storage.base import StorageService

ingest_router = APIRouter(
    prefix=str(Path(API_PREFIX_PATH) / "ingest"),
    tags=["Data Ingestion Service"]
)

@ingest_router.post("/upload/{project_id}")
async def upload_file(
    project_id: str,
    file: UploadFile,
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
):
    upload_service = UploadService(
        sts=storage_service
    )

    await upload_service.upload(
        project_id=project_id, 
        file=file
    )

    return {
        "status": "ok", 
        "message": "documents is uploaded successfully."
    }

