from datetime import datetime, timezone
from pydantic import BaseModel, Field, UUID4
from typing import Optional
import json 


class XRAGModel(BaseModel):

    def asbytes(self):
        return (
            self.model_dump_json().encode("utf-8")
        )

    def asdict(self) -> dict:
        return self.model_dump()

    @classmethod
    def load(
        cls, 
        json_data: dict | bytes
    ):
        return cls.model_validate_json(json_data=json_data)


class Page(XRAGModel):
    page: int = Field(..., ge=1)
    content: str
    width: Optional[int] = None
    height: Optional[int] = None


class Document(XRAGModel):
    pages: list[Page]


class ChunkMetadata(XRAGModel):
    workspace_id: str
    document_id: str 
    page: int = Field(ge=0)
    chunk_id: UUID4
    chunk_size: int = Field(ge=1)
    chunk_overlap: int = Field(ge=1)
    embedding_model: str
    embedding_provider: str


class Chunk(XRAGModel):
    id_: UUID4
    text: str

    metadata: ChunkMetadata


class ChunkList(XRAGModel):
    chunks: list[Chunk]


class RetrievedSnippet(XRAGModel):
    text: str 
    score: float

    metadata: dict = Field(default_factory=dict)

class AugmentedQuery(XRAGModel):

    query: str
    ctx: list[RetrievedSnippet]

    # TODO: Add History Messages

    @property
    def instructions(
        self
    ) -> str:
        return "\n".join([
            "You are a RAG question-answering assistant.",
            "Answer the user's question using only the provided context.",
            "Rules:",
            "- Do not use outside knowledge.",
            "- If the answer cannot be found in the context, say that the provided documents do not contain enough information.",
            "- Be concise and precise.",
            "- Cite sources using [Source N].",
            "- Do not invent citations.",
        ])

    @property
    def input(self) -> str:
        return "\n".join([
            "Question:", f"{self.query}", "Retrieved context:", f"{self.context}"
        ])

    @property
    def context(self) -> str:
        return "\n\n".join([
            f"## Chunk {i}:\n {s.text}"
            for i, s in enumerate(self.ctx)
        ])