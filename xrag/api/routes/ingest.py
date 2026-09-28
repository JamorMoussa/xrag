from fastapi import APIRouter, Depends, UploadFile
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel
from llama_index.core import Document
from temporalio.client import Client
import uuid

from xrag.configs import API_PREFIX_PATH
from ..deps import (
    get_storage_service, get_liteparser_service, get_temporal_client, get_configs
)
from xrag.services.ingest.upload import UploadService
from xrag.services.storage import StorageService, File
from xrag.services.ingest.parse import LiteParserService
from xrag.configs import Configs

class ParseRequest(BaseModel):
    object_key: str

ingest_router = APIRouter(
    prefix=str(Path(API_PREFIX_PATH) / "ingest"),
    tags=["Data Ingestion Service"]
)

@ingest_router.post("/upload/{project_id}")
async def upload(
    project_id: str,
    file: UploadFile,
    storage_service: Annotated[StorageService, Depends(get_storage_service)],
):
    upload_service = UploadService(
        sts=storage_service
    )

    object_key = await upload_service.upload(
        project_id=project_id, 
        file=file
    )

    return {
        "status": "ok", 
        "message": "documents is uploaded successfully.",
        "object_key": object_key
    }

@ingest_router.post("/parse")
async def parse(
    request: ParseRequest, 
    client: Annotated[Client, Depends(get_temporal_client)],
    configs: Annotated[Configs, Depends(get_configs)],
):

    workflow_id = f"ingestion-{uuid.uuid4()}"

    results = await client.start_workflow(
        "IngestionWorkflow",
        args=[
            {
                "object_key": request.object_key,
            }
        ],
        id=workflow_id,
        task_queue=configs.TEMPORAL_TASK_QUEUE,
        result_type=dict,
    )

    return {
        "workflow_id": workflow_id
    }

    
