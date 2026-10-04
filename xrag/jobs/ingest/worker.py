from temporalio.client import Client
from temporalio.worker import Worker
import asyncio

from xrag.jobs.ingest.workflows import IngestionWorkflow
from xrag.jobs.ingest.activities import (
    ParsingActivity, ChunkingActivity
)
from xrag.configs import configs

async def main():

    temporal_client = await Client.connect(
        configs.TEMPORAL_HOST,
        namespace=configs.TEMPORAL_NAMESPACE,
    )

    parse_activity = ParsingActivity(configs=configs).parse
    chunk_activity = ChunkingActivity(configs=configs).chunk

    worker_ingest_process = Worker(
        temporal_client,
        task_queue=configs.TEMPORAL_TASK_QUEUE,
        workflows=[IngestionWorkflow],
        activities=[parse_activity, chunk_activity],
    )

    await worker_ingest_process.run()


if __name__ == "__main__":
    asyncio.run(main())