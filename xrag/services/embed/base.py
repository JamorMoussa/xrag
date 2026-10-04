from abc import ABC, abstractmethod
import httpx

from xrag.configs import Configs


class EmbeddingService(ABC):

    def __init__(
        self,
        configs: Configs
    ):
        self.configs = configs

        self.client = self.get_client(
            configs=configs
        )

    def get_client(
        self, 
        configs: Configs
    ) -> httpx.Client:
        return httpx.AsyncClient(
            base_url=configs.EMBEDDING_BASE_URL,
            timeout=120.0,
        )

    @abstractmethod
    def embed(
        self, 
        text: list[str]
    ):
        ... 