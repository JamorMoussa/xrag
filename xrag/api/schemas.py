from pydantic import BaseModel
from typing import Literal, Optional


class UploadArgs(BaseModel):
    workspace_id: str
    storage_type: Literal["raw", "parsed", "chunks"] = "raw"
    document_id: Optional[str] = None

class DownloadArgs(BaseModel):
    workspace_id: str
    document_id: str
    ext: str
    storage_type: Literal["raw", "parsed", "chunks"] = "raw"


class ParseArgs(BaseModel):
    workspace_id: str
    document_id: str
    ext: str
