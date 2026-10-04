from datetime import datetime, timezone
from pydantic import BaseModel, Field, UUID4
from typing import Optional


class Page(BaseModel):
    page: int = Field(..., ge=1)
    content: str
    width: Optional[int] = None
    height: Optional[int] = None


class Document(BaseModel):
    pages: list[Page]


class ChunkMetadata(BaseModel):
    workspace_id: str
    document_id: str 
    page: int = Field(ge=0)
    chunk_id: UUID4
    chunk_size: int = Field(ge=1)
    chunk_overlap: int = Field(ge=1)


class Chunk(BaseModel):
    id_: UUID4
    text: str

    metadata: ChunkMetadata


class ChunkList(BaseModel):
    chunks: list[Chunk]
