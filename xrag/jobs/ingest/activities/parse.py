from temporalio import activity

from xrag.jobs.ingest.schemas import IngestArgs
from xrag.services.storage import (
    StorageService, PathObject, FileObject
)
from xrag.services.ingest.parse import ParserService


class ParsingActivity:

    def __init__(
        self,
        storage_service: StorageService,
        parser_service: ParserService
    ):
        self.storage_service = storage_service
        self.parser_service = parser_service

    @activity.defn
    async def parse(
        self,
        args: IngestArgs
    ) -> IngestArgs:

        path_parsed = PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id,
                document_type="parsed"
        )

        file: FileObject = self.storage_service.load(
            path=PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id
            )
        )

        document = await self.parser_service.parse(
            content=file.content,
            filename=file.filename,
            content_type=file.content_type,
        )

        self.storage_service.save(
            file=FileObject(
                content=document.model_dump_json().encode("utf-8"),
                filename="parsed.json",
                content_type="application/json"
            ),
            path=path_parsed
        )

        return args.model_copy(
            update={
                "parsed_key": path_parsed.key 
            }
        )
