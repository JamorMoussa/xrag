from fastapi import APIRouter
from pathlib import Path
from pydantic import BaseModel

from xrag.configs import configs
from xrag.models import RetrievedSnippet
from xrag.deps import RetrievalDep

retrieve_router = APIRouter(
    prefix= str(
        Path(configs.API_PREFIX_PATH) / "r"
    )
)

class Query(BaseModel):
    query: str
    top_k: int = 5
    do_rerank: bool = True

@retrieve_router.post("/retrieve")
async def retrieve(
    query: Query,
    retrieve_service: RetrievalDep
) -> list[RetrievedSnippet]:

    # TODO: impl the re-ranking method for best retrieving resutls.
    return (
        await retrieve_service.search(
            query=query.query, top_k=query.top_k, do_rerank=query.do_rerank
        )
    )