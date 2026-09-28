from temporalio.client import Client
from temporalio.worker import Worker
import asyncio

from xrag.tasks.workflows import IngestionWorkflow
from xrag.tasks.activities import (
    parse_activity
)
from xrag.configs import Configs

configs = Configs()

async def main():
    temporal_client = await Client.connect(
        configs.TEMPORAL_HOST,
        namespace=configs.TEMPORAL_NAMESPACE,
    )

    worker_pdf_process = Worker(
        temporal_client,
        task_queue=configs.TEMPORAL_TASK_QUEUE,
        workflows=[IngestionWorkflow],
        activities=[parse_activity],
    )

    await worker_pdf_process.run()


if __name__ == "__main__":
    asyncio.run(main())