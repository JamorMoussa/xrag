from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional


class Page(BaseModel):
    page: int = Field(..., ge=1)
    content: str
    width: Optional[int] = None
    height: Optional[int] = None


class Document(BaseModel):
    pages: list[Page]