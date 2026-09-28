from abc import ABC, abstractmethod
from dataclasses import dataclass

from xrag.configs import Configs

@dataclass
class File:
    content: bytes
    filename: str
    content_type: str
    

class StorageService(ABC):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__()
        self.configs = configs

    @abstractmethod
    async def upload():
        ...

    @abstractmethod
    async def delete():
        ...

    @abstractmethod
    async def download():
        ...
