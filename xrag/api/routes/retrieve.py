from fastapi import APIRouter, Depends
from pathlib import Path
from pydantic import BaseModel
from typing import Annotated

from xrag.configs import configs
from xrag.services.retrieve import RetrievalService
from ..deps import get_retrieve_service

retreive_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "r"
    )
)

class Query(BaseModel):
    query: str 

@retreive_router.get("/retrieve")
async def retrieve(
    query: Query,
    retrieve_service: Annotated[RetrievalService, Depends(get_retrieve_service)]
):
    return await retrieve_service.search(
        query=query.query
    )