from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Iterator
from typing import BinaryIO
from enum import Enum
from uuid import uuid4

from src.configs import Configs

@dataclass
class StorageFile:
    content: BinaryIO | Iterator[bytes]
    filename: str
    content_type: str

class StorageType(Enum):
    RAW = "raw"
    PARSED = "parsed"
    CHUNKED = "chunks"

@dataclass
class StorageKey:
    document_id: str
    workspace_id: str
    storage_type: StorageType
    content_type: str 
    ext: str
    

class StorageService(ABC):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__()
        self.configs = configs

    def _generate_key(
        self, 
        storage_key: StorageKey
    ):

        name = None 

        if storage_key.storage_type is StorageType.RAW:
            name = storage_key.document_id
        else:
            name = storage_key.storage_type.value

        return "/".join([
            storage_key.workspace_id,
            storage_key.document_id,
            f"{name}.{storage_key.ext}"
        ])

    @abstractmethod
    def upload(
        self,
        storage_file: StorageFile, 
        storage_key: StorageKey
    ):
        ...

    @abstractmethod
    def delete():
        ...

    @abstractmethod
    def download(
        object_key: str 
    ) -> StorageFile:
        ...
