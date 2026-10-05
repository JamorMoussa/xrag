from xrag.configs import Configs
from xrag.services.embed import OpenAIEmbeddingService
from xrag.services.vecdb import QdrantVecDBService
from xrag.models import ContextSnippet


class RetrievalService:

    def __init__(
        self,
        configs: Configs
    ):

        self.embed_service = OpenAIEmbeddingService(configs=configs)

        self.vecdb_service = QdrantVecDBService(configs=configs)

    async def search(
        self, 
        query: str,
        top_k: int = 5,
    ) -> list[ContextSnippet]:
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