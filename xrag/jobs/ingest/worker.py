from temporalio.client import Client
from temporalio.worker import Worker
import asyncio

from xrag.jobs.ingest.workflows import IngestionWorkflow
from xrag.jobs.ingest.activities import (
    ParseActivity
)
from xrag.configs import configs

async def main():

    temporal_client = await Client.connect(
        configs.TEMPORAL_HOST,
        namespace=configs.TEMPORAL_NAMESPACE,
    )

    parse_activity = ParseActivity(configs=configs).parse

    worker_ingest_process = Worker(
        temporal_client,
        task_queue=configs.TEMPORAL_TASK_QUEUE,
        workflows=[IngestionWorkflow],
        activities=[parse_activity],
    )

    await worker_ingest_process.run()


if __name__ == "__main__":
    asyncio.run(main())