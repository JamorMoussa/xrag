from temporalio import workflow
from datetime import timedelta

with workflow.unsafe.imports_passed_through():
    from .activities import (
        parse_activity
    )

    from .schemas import ParseOutput, ParseInput

@workflow.defn
class IngestionWorkflow:

    @workflow.run
    async def run(self, input: ParseInput) -> ParseOutput:

        parsed_result = await workflow.execute_activity(
            parse_activity,
            ParseInput(object_key=input.object_key),
            start_to_close_timeout=timedelta(minutes=3),
        )

        return ParseOutput(
            parsed_object_key=parsed_result["parsed_object_key"]
        )