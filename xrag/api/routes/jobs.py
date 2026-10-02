from fastapi import APIRouter, status
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from uuid import uuid4
from pathlib import Path

from xrag.api.schemas import DownloadArgs
from xrag.configs import configs

jobs_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "jobs"
    )
)


@jobs_router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest(args: DownloadArgs) -> dict:

    client = await Client.connect(
        configs.TEMPORAL_HOST,
        namespace=configs.TEMPORAL_NAMESPACE,
        data_converter=pydantic_data_converter,
    )

    handle = await client.start_workflow(
        "IngestionWorkflow",
        args,
        id=f"ingestion-{args.workspace_id}-{args.document_id}-{uuid4()}",
        task_queue=configs.TEMPORAL_TASK_QUEUE,
    )

    return {
        "status": "started",
        "workflow_id": handle.id,
        "document_id": args.document_id,
    }