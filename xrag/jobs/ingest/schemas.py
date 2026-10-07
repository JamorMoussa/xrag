from pydantic import BaseModel, Field
from typing import Literal, Optional


class IngestArgs(BaseModel):
    workspace_id: str
    document_id: str

    parsed_key: Optional[str] = Field(default_factory=lambda: None)
    chunked_key: Optional[str] = Field(default_factory=lambda: None)
