from abc import ABC, abstractmethod

from xrag.configs import Configs

class ParserService(ABC):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__()
        self.configs = configs

    @abstractmethod
    async def parse(
        self,
        content: bytes,
        filename: str,
        content_type: str,  
    ):
        ...