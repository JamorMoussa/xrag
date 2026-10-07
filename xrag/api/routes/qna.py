from fastapi import APIRouter
from pathlib import Path
from pydantic import BaseModel

from xrag.configs import configs
from xrag.models import AugmentedQuery
from xrag.deps import RetrievalDep, QnADep

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
    retrieve_service: RetrievalDep,
    qna_service: QnADep
) -> dict:

    # TODO: impl the re-ranking method for best retrieving resutls.
    snippets = (
        await retrieve_service.search(
            query=query.query, top_k=query.top_k
        )
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