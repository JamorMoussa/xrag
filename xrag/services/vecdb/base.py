from abc import ABC, abstractmethod

from xrag.models import Chunk


class VecDBService(ABC):

    @abstractmethod
    def upsert(
        self,
        chunks: list[Chunk],
        embeddings: list[float]
    ):
        ... 

    # TODO: add search function.