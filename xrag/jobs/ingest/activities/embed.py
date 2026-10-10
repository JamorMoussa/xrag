from temporalio import activity

from xrag.jobs.ingest.schemas import IngestArgs
from xrag.services.storage import (
    StorageService, PathObject, FileObject
)
from xrag.models import ChunkList, Chunk
from xrag.services.embed import EmbeddingService
from xrag.services.vecdb import VecDBService


class EmbeddingActivity:

    def __init__(
        self,
        storage_service: StorageService,
        embed_service: EmbeddingService,
        vecdb_service: VecDBService
    ):
        self.storage_service = storage_service
        self.embed_service = embed_service
        self.vecdb_service = vecdb_service

    @activity.defn
    async def embed(
        self, 
        args: IngestArgs
    ) -> IngestArgs:

        batch_size: int = 32

        file: FileObject = self.storage_service.load(
            path=PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id,
                document_type="chunks"
            )
        )

        chunks = ChunkList.model_validate_json(
            file.content
        ).chunks

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            await self.embed_upsert(
                chunks=batch
            )

        return args

    async def embed_upsert(
        self, 
        chunks: list[Chunk]
    ):
        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = (
            await self.embed_service.embed(texts=texts)
        )      

        await self.vecdb_service.upsert(
            chunks=chunks, embeddings=embeddings
        )
