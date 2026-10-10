from qdrant_client import AsyncQdrantClient, models
from typing import Literal

from .base import VecDBService
from xrag.models import Chunk, RetrievedSnippet
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
                vectors_config={
                    "dense": models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE,
                    )
                },
                sparse_vectors_config={
                    "bm25": models.SparseVectorParams(
                        modifier=models.Modifier.IDF
                    )
                }
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
            models.PointStruct(
                id=chunk.id_,
                vector={
                    "dense": embedding,
                    "bm25": models.Document(
                        text=chunk.text,
                        model="Qdrant/bm25"
                    )
                },
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
            points=points, wait=True
        )


    async def search(
        self,
        query: str,
        query_embedding: list[float],
        top_k: int = 5,
        mode: Literal["dense", "sparse", "hybrid"] = "hybrid"
    ) -> list[RetrievedSnippet]:

        search_args: dict = None 
        
        if mode == "dense":
            search_args = {
                "query": query_embedding,
                "using": "dense",
            }

        elif mode == "sparse":
            search_args = {
                "query": models.Document(
                    text=query,
                    model="Qdrant/bm25",
                ),
                "using": "bm25",
            }

        elif mode == "hybrid":

            prefetch_limit = max(top_k, 30)

            search_args = {
                "prefetch": [
                    models.Prefetch(
                        query=query_embedding,
                        using="dense",
                        limit=prefetch_limit,
                    ),
                    models.Prefetch(
                        query=models.Document(
                            text=query,
                            model="Qdrant/bm25",
                        ),
                        using="bm25",
                        limit=prefetch_limit,
                    ),
                ],
                "query": models.FusionQuery(
                    fusion=models.Fusion.RRF
                ),
            }
        
        result = await self.client.query_points(
            collection_name=self.configs.VECDB_COLLECTION,
            **search_args,
            # TODO: add filter over workspaceid if necessary
            # query_filter=...
            limit=top_k,
            with_payload=True
        )

        result = result.points

        return [
            RetrievedSnippet(
                text=r.payload["text"], score=r.score, 
                metadata={
                    k:v for k, v in r.payload.items() if k != "text"
                }
            )
            for r in result
        ]