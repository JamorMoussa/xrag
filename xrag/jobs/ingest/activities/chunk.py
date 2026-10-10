from temporalio import activity
import json 

from xrag.configs import Configs
from xrag.jobs.ingest.schemas import IngestArgs
from xrag.services.storage import (
    StorageService, PathObject, FileObject
)
from xrag.models import Document
from xrag.services.ingest.chunk import ChunkingStrategy


class ChunkingActivity:


    def __init__(
        self, 
        configs: Configs,
        storage_service: StorageService,
        chunking_strategy: ChunkingStrategy,
    ):
        self.configs = configs
        self.storage_service = storage_service
        self.chunking_strategy = chunking_strategy

    @activity.defn
    async def chunk(
        self,
        args: IngestArgs
    ) -> dict:

        file: FileObject = self.storage_service.load(
            path=PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id,
                document_type="parsed"
            )
        )

        chunk_list = (
            self.chunking_strategy.chunk(
                docs=Document(
                    **json.loads(file.content)
                ),
                metadata={
                    "workspace_id": args.workspace_id,
                    "document_id": args.document_id
                }
            )
        )

        self.storage_service.save(
            file=FileObject(
                content=chunk_list.asbytes(),
                filename="chunks.json",
                content_type="application/json"
            ),
            path=PathObject(
                workspace_id=args.workspace_id, document_id=args.document_id, document_type="chunks"
            )
        )

        return {
            "chunks_key": PathObject(
                workspace_id=args.workspace_id, document_id=args.document_id, document_type="chunks"
            ).key
        }