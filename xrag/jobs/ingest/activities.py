from temporalio import activity
from io import BytesIO

from xrag.configs import Configs
from xrag.api.schemas import ParseArgs
from xrag.services.storage import (
    StorageType, S3StorageService, File, StorageKey
)
from xrag.services.ingestion.parse import LiteParserService
from xrag.utils import get_object_key


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
        args: ParseArgs
    ):

        # TODO: Make code as utils to use here, and in /download endpoint.

        key = get_object_key(
            workspace_id=args.workspace_id,
            document_id=args.document_id,
            name=args.document_id,
            ext=args.ext
        )

        file = self.storage_service.download(
            object_key=key
        )

        document = await self.parser.parse(
            content=file.content,
            filename=file.filename,
            content_type=file.content_type,
        )

        key = self.storage_service.upload(
            file=File(
                content=BytesIO(document.model_dump_json().encode("utf-8")),
                filename="parsed.json", 
                content_type="application/json"
            ),
            storage_key=StorageKey(
                document_id=args.document_id,
                workspace_id=args.workspace_id,
                storage_type=StorageType("parsed"),
                content_type="application/json",
                ext=".json"
            )
        )

        return {
            "status": "parsed",
            "key": key
        }