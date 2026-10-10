from abc import ABC, abstractmethod

from xrag.models import Document, ChunkList
from xrag.configs import Configs

class ChunkingStrategy(ABC):

    def __init__(
        self, 
        configs: Configs
    ):
        self.configs = configs

    @abstractmethod
    def chunk(
        self, 
        docs: list[Document],
        metadata: dict
    ) -> ChunkList:
        ... 