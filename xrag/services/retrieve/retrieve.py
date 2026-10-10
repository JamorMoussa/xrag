from typing import Literal

from xrag.services.embed import EmbeddingService
from xrag.services.vecdb import VecDBService
from .rerank import ReRankerService
from xrag.models import RetrievedSnippet


class RetrievalService:

    def __init__(
        self,
        embed_service: EmbeddingService,
        vecdb_service: VecDBService,
        reranker_service: ReRankerService
    ):
        self.embed_service = embed_service
        self.vecdb_service = vecdb_service
        self.reranker_service = reranker_service

    async def search(
        self, 
        query: str,
        top_k: int = 5,
        do_rerank: bool = True,
        retrieve_mode: Literal["dense", "sparse", "hybrid"] = "hybrid"
    ) -> list[RetrievedSnippet]:
        
        embeddings = (
            await self.embed_service.embed(
                texts=query
            )
        )

        results = await self.vecdb_service.search(
            query=query,
            query_embedding=embeddings[0],
            top_k= (top_k * 3) if do_rerank else top_k,
            mode=retrieve_mode
        )

        if do_rerank:
            results = await self.reranker_service.rerank(
                query=query, snippets=results, top_k=top_k
            )

        return results