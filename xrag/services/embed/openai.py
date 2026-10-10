import httpx

from xrag.configs import Configs
from .base import EmbeddingService

class OpenAIEmbeddingService(EmbeddingService):

    client: httpx.Client

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__(configs=configs)


    async def embed(
        self, 
        texts: list[str] | str
    ):
        if isinstance(texts, str):
            texts = [texts]

        response = await self.client.post(
            "/embeddings",
            json={
                "model": self.configs.EMBEDDING_MODEL,
                "input": texts,
            },
        )

        response.raise_for_status()

        data = response.json()["data"]

        return [
            item["embedding"]
            for item in sorted(
                data,
                key=lambda item: item["index"],
            )
        ]