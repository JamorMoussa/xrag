from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

from .base import VecDBService
from xrag.models import Chunk, ContextSnippet
from xrag.configs import Configs


class QdrantVecDBService(VecDBService):


    def __init__(
        self,
        configs: Configs
    ):
        self.configs = configs

        self.client = AsyncQdrantClient(
            url=self.configs.VECDB_BASE_URL
        )

    async def ensure_collection(
        self,
        vector_size: int,
    ) -> None:

        exists = await self.client.collection_exists(
            collection_name=self.configs.VECDB_COLLECTION
        )

        if not exists:
            await self.client.create_collection(
                collection_name=self.configs.VECDB_COLLECTION,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    async def upsert(
        self,
        chunks: list[Chunk],
        embeddings: list[float]
    ):

        await self.ensure_collection(
            vector_size=len(embeddings[0])
        )

        points = [
            PointStruct(
                id=chunk.id_,
                vector=embedding,
                payload={
                    **chunk.metadata.asdict(),
                    "text": chunk.text,
                },
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
            )
        ]

        await self.client.upsert(
            collection_name=self.configs.VECDB_COLLECTION,
            points=points,
        )


    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 5
    ) -> list[ContextSnippet]:
        
        result = await self.client.query_points(
            collection_name=self.configs.VECDB_COLLECTION,
            query=query_embedding,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        result = result.points

        return [
            ContextSnippet(
                text=r.payload["text"], score=r.score, 
                metadata={
                    k:v for k, v in r.payload.items() if k != "text"
                }
            )
            for r in result
        ]