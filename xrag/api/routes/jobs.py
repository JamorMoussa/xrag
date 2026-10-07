from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.client import Client

from fastapi import APIRouter, status
from pathlib import Path
from uuid import uuid4

from xrag.services.storage import PathObject
from xrag.exceptions import DocumentNotFoundError
from xrag.deps import StorageDep
from xrag.configs import configs


jobs_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "jobs"
    )
)


@jobs_router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest(
    path: PathObject,
    storage_service: StorageDep,
) -> dict:

    if not storage_service.raw_exists(path=path):
        raise DocumentNotFoundError(
            key=path.key
        )

    client = await Client.connect(
        configs.TEMPORAL_HOST,
        namespace=configs.TEMPORAL_NAMESPACE,
        data_converter=pydantic_data_converter,
    )

    handle = await client.start_workflow(
        "IngestionWorkflow",
        path,
        id=f"ingestion-{path.workspace_id}-{path.document_id}-{uuid4()}",
        task_queue=configs.TEMPORAL_TASK_QUEUE,
    )

    return {
        "status": "started",
        "workflow_id": handle.id,
        "document_id": path.document_id,
    }