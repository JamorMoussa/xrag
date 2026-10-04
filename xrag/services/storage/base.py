from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum 
from uuid import uuid4

from xrag.configs import Configs


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class FileObject(BaseModel):
    content: bytes 
    filename: str 
    content_type: str


class PathObject(BaseModel):
    workspace_id: str
    document_id: Optional[str] = None
    document_type: Literal["raw", "parsed", "chunks", "manifest"] = "raw"
    is_new: bool = False

    @model_validator(mode="before")
    @classmethod
    def set_document_id(cls, data):
        if not data.get("document_id"):
            data["document_id"] = uuid4().hex
            data["is_new"] = True

        return data

    @property
    def key(self):
        return "/".join([
            self.workspace_id,
            self.document_id,
            self.filename,
        ])

    @property
    def filename(self):
        return (
            self.document_type
            if self.document_type == "raw"
            else f"{self.document_type}.json"
        )



class ArtifactType(str, Enum):
    RAW = "raw"
    PARSED = "parsed"
    CHUNKS = "chunks"
    MANIFEST = "manifest"

class Artifact(BaseModel):
    type_: ArtifactType
    filename: Optional[str] = Field(default_factory=lambda: None)
    content_type: str
    updated_at: datetime = Field(default_factory=utc_now)

class Manifest(BaseModel):

    schema_version: int = 1
    workspace_id: str 
    document_id: str

    content_type: str = Field(default_factory=lambda: "application/json")
    create_at: datetime = Field(default_factory=utc_now)
    uplated_at: datetime = Field(default_factory=utc_now)

    artifacts: dict[ArtifactType, Artifact] = Field(
        default_factory=dict
    )

    def asbytes(self) -> bytes:
        return self.model_dump_json().encode("utf-8")

    def add_artifact(
        self, 
        artifact: Artifact
    ):
        self.artifacts[artifact.type_] = artifact

    def get_artifact(
        self, 
        kind: ArtifactType
    ):
        try:
            return self.artifacts[kind]
        except KeyError:
            raise ValueError(
                f"Document {self.document_id} has no {kind.value} artifact"
            ) from None



class StorageService(ABC):
    ... 

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__()
        self.configs = configs

    @abstractmethod
    def save(
        self, 
        file: FileObject, 
        path: PathObject, 
    ):
        ...

    @abstractmethod
    def load(
        self,
        path: PathObject
    ) -> FileObject:
        ... 


    @abstractmethod
    def load_manifest(
        self, 
        path: PathObject
    ) -> Manifest:
        ... 

    @abstractmethod
    def save_manifest(
        self, 
        path: PathObject,
        manifest: Manifest
    ):
        ...

    @abstractmethod
    def raw_exists(
        self, path: PathObject
    ) -> bool:
        ... 