from temporalio import activity

from xrag.configs import Configs
from xrag.api.schemas import IngestArgs
from xrag.services.storage import (
    S3StorageService, PathObject, FileObject
)
from xrag.services.ingestion.parse import LiteParserService


class ParseActivity:

    def __init__(
        self, 
        configs: Configs
    ):
        self.configs = configs

        self.storage_service = S3StorageService(
            configs=configs
        )

        self.parser = LiteParserService(
            configs=configs
        )

    @activity.defn
    async def parse(
        self,
        args: IngestArgs
    ):

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

        document = await self.parser.parse(
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

        return {
            "status": "parsed",
            "key": path_parsed.key
        }