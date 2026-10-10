from abc import ABC, abstractmethod
from typing import Literal

from xrag.models import Chunk, RetrievedSnippet


class VecDBService(ABC):

    @abstractmethod
    def upsert(
        self,
        chunks: list[Chunk],
        embeddings: list[float]
    ):
        ... 

    # TODO: add search function.

    async def search(
        self,
        query: str,
        query_embedding: list[float],
        top_k: int = 5,
        mode: Literal["dense", "sparse", "hybrid"] = "hybrid"
    ) -> list[RetrievedSnippet]:
        ...