from abc import ABC, abstractmethod

from xrag.configs import Configs

class StorageService(ABC):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__()
        self.configs = configs

    @abstractmethod
    async def upload_file():
        ...

    @abstractmethod
    async def delete_file():
        ...
