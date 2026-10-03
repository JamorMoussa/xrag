from temporalio import workflow
from datetime import timedelta

with workflow.unsafe.imports_passed_through():
    from .activities import (
        ParseActivity
    )
    from xrag.api.schemas import IngestArgs

@workflow.defn
class IngestionWorkflow:
    @workflow.run
    async def run(
        self, 
        args: IngestArgs
    ) -> dict:

        result = await workflow.execute_activity_method(
            ParseActivity.parse,
            args,
            start_to_close_timeout=timedelta(minutes=3),
        )

        return result
