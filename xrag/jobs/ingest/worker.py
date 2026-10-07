from temporalio.client import Client
from temporalio.worker import Worker
import asyncio

from xrag.jobs.ingest.workflows import IngestionWorkflow
from xrag.jobs.ingest.activities import (
    ParsingActivity, ChunkingActivity, EmbeddingActivity
)
from xrag.configs import configs

from xrag.deps.services import (
    get_storage_service,
    get_embed_service,
    get_vecdb_service,
    get_parser_service,
)

async def main():

    temporal_client = await Client.connect(
        configs.TEMPORAL_HOST,
        namespace=configs.TEMPORAL_NAMESPACE,
    )


    storage_service = get_storage_service(
        configs=configs,
    )

    embed_service = get_embed_service(
        configs=configs,
    )

    vecdb_service = get_vecdb_service(
        configs=configs,
    )

    parser_service = get_parser_service(
        configs=configs,
    )

    parse_activity = (
        ParsingActivity(
            storage_service=storage_service, parser_service=parser_service
        ).parse
    )

    chunk_activity = (
        ChunkingActivity(
            configs=configs, storage_service=storage_service
        ).chunk
    )

    embed_activity = (
        EmbeddingActivity(
            storage_service=storage_service, embed_service=embed_service, vecdb_service=vecdb_service
        ).embed
    )

    worker_ingest_process = Worker(
        temporal_client,
        task_queue=configs.TEMPORAL_TASK_QUEUE,
        workflows=[IngestionWorkflow],
        activities=[parse_activity, chunk_activity, embed_activity],
    )

    await worker_ingest_process.run()


if __name__ == "__main__":
    asyncio.run(main())