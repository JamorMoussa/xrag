from fastapi import APIRouter, Depends
from pathlib import Path
from pydantic import BaseModel
from typing import Annotated

from xrag.configs import configs
from xrag.models import RetrievedSnippet
from xrag.services.retrieve import RetrievalService
from ..deps import get_retrieve_service

retrieve_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "r"
    )
)

class Query(BaseModel):
    query: str
    top_k: int = 5

@retrieve_router.post("/retrieve")
async def retrieve(
    query: Query,
    retrieve_service: Annotated[RetrievalService, Depends(get_retrieve_service)]
) -> list[RetrievedSnippet]:

    # TODO: impl the re-ranking method for best retrieving resutls.
    return await retrieve_service.search(
        query=query.query, top_k=query.top_k
    )