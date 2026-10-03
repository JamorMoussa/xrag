from pydantic import BaseModel
from typing import Literal, Optional


class IngestArgs(BaseModel):
    workspace_id: str
    document_id: str
