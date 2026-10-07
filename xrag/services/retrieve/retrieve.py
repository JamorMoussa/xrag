from xrag.services.embed import EmbeddingService
from xrag.services.vecdb import VecDBService
from xrag.models import RetrievedSnippet


class RetrievalService:

    def __init__(
        self,
        embed_service: EmbeddingService,
        vecdb_service: VecDBService
    ):
        self.embed_service = embed_service
        self.vecdb_service = vecdb_service

    async def search(
        self, 
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedSnippet]:
        embeddings = (
            await self.embed_service.embed(
                texts=query
            )
        )

        results = await self.vecdb_service.search(
            query_embedding=embeddings[0],
            top_k=top_k,
        )

        return results