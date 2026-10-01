from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Iterator
from typing import BinaryIO
from enum import Enum
from uuid import uuid4

from xrag.configs import Configs

@dataclass
class File:
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

    def get_key(
        self, 
    ):

        name = None 

        if self.storage_type is StorageType.RAW:
            name = self.document_id
        else:
            name = self.storage_type.value

        return "/".join([
            self.workspace_id,
            self.document_id,
            f"{name}.{self.ext}"
        ])
    

class StorageService(ABC):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__()
        self.configs = configs

    @abstractmethod
    def upload(
        self,
        file: File, 
        storage_key: StorageKey
    ):
        ...

    @abstractmethod
    def delete():
        ...

    @abstractmethod
    def download(
        object_key: str 
    ) -> File:
        ...
