from temporalio import workflow
from datetime import timedelta

with workflow.unsafe.imports_passed_through():
    from xrag.jobs.ingest.activities.parse import ParsingActivity
    from xrag.jobs.ingest.activities.chunk import ChunkingActivity
    from xrag.jobs.ingest.activities.embed import EmbeddingActivity
    from .schemas import IngestArgs

@workflow.defn
class IngestionWorkflow:
    @workflow.run
    async def run(
        self, 
        args: IngestArgs
    ) -> dict:

        await workflow.execute_activity_method(
            ParsingActivity.parse,
            args,
            start_to_close_timeout=timedelta(minutes=3),
        )

        await workflow.execute_activity_method(
            ChunkingActivity.chunk,
            args,
            start_to_close_timeout=timedelta(minutes=3),
        )

        await workflow.execute_activity_method(
            EmbeddingActivity.embed,
            args,
            start_to_close_timeout=timedelta(minutes=3),
        )

        return {
            "status": "ok"
        }
