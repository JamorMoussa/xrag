from temporalio import activity
from llama_index.core import Document
from io import BytesIO
import json 

from ..services.storage import S3StorageService
from ..services.ingest.parse import LiteParserService
from .schemas import ParseInput, ParseOutput
from xrag.configs import Configs

configs = Configs()

class ParseActivity:

    def __init__(
        self, 
        storage: S3StorageService, 
        parser: LiteParserService
    ):
        self.storage = storage
        self.parser = parser

    @activity.defn
    async def parse(
        self, input: ParseInput
    ):

        file = await (
            self.storage.download(
                object_key=input.object_key
            )
        )

        documents: list[Document] = await self.parser.parse(
            content=file.content, 
            filename=file.filename, 
            content_type=file.content_type
        )

        parsed = [
            {
                "content": doc.text,
                "metadata": {
                    "id": doc.id_,
                    "filename": str(doc.metadata["filename"]),
                    "page": doc.metadata["page"],
                },
            }
            for doc in documents
        ]

        project_id = input.object_key.split("/")[0]

        parsed_object_key = (
            project_id + "/ingest/parsed.json"
        )

        await self.storage.upload(
            object_key=parsed_object_key, 
            fileobj=BytesIO(
                json.dumps(parsed).encode("utf-8")
            ),
            content_type="application/json"
        )

        return ParseOutput(
            parsed_object_key=parsed_object_key
        )

parse_activity = ParseActivity(
    storage=S3StorageService(configs=configs), 
    parser=LiteParserService(configs=configs)
).parse



        