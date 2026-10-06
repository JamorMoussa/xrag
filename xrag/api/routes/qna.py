from fastapi import APIRouter, Depends
from pathlib import Path
from pydantic import BaseModel
from typing import Annotated

from xrag.configs import configs
from xrag.models import AugmentedQuery
from xrag.services.retrieve import RetrievalService
from xrag.services.qna import QnAService
from ..deps import get_retrieve_service, get_qna_service

qna_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "q"
    )
)

class Query(BaseModel):
    query: str
    top_k: int = 5

@qna_router.post("/ask")
async def ask(
    query: Query,
    retrieve_service: Annotated[RetrievalService, Depends(get_retrieve_service)],
    qna_service: Annotated[QnAService, Depends(get_qna_service)]
) -> dict:

    # TODO: impl the re-ranking method for best retrieving resutls.
    snippets = await retrieve_service.search(
        query=query.query, top_k=query.top_k
    )

    # TODO: support for stream generation:
    answer = await qna_service.ask(
        query=AugmentedQuery(
            query=query.query,
            ctx=snippets
        )
    )

    return {
        "answer": answer
    }