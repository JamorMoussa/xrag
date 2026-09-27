from abc import ABC, abstractmethod


class StorageService(ABC):

    @abstractmethod
    async def upload():
        ...

    @abstractmethod
    async def delete():
        ...
