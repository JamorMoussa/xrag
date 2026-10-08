from fastapi import Depends
from typing import Annotated
from temporalio.client import Client

from xrag.configs import Configs, get_configs
from xrag.services.storage import StorageService
from xrag.services.embed import EmbeddingService
from xrag.services.vecdb import VecDBService
from xrag.services.retrieve import RetrievalService, ReRankerService
from xrag.services.ingest.parse import ParserService
from xrag.services.qna import QnAService
from xrag.services.qna.llms import ChatService

from .services import (
    get_storage_service, get_embed_service, get_vecdb_service,
    get_retrieval_service, get_parser_service, get_qna_service,
    get_chat_service, get_temporal_client, get_rerank_service
)

ConfigsDep = Annotated[
    Configs,
    Depends(get_configs),
]

def storage_dep(
    configs: ConfigsDep,
) -> StorageService:
    return get_storage_service(configs)

StorageDep = Annotated[
    StorageService,
    Depends(storage_dep),
]

def embed_dep(
    configs: ConfigsDep,
) -> EmbeddingService:
    return get_embed_service(configs)


EmbeddingDep = Annotated[
    EmbeddingService,
    Depends(embed_dep),
]

def vecdb_dep(
    configs: ConfigsDep,
) -> VecDBService:
    return get_vecdb_service(configs)


VecDBDep = Annotated[
    VecDBService,
    Depends(vecdb_dep),
]

def chat_dep(
    configs: ConfigsDep
) -> ChatService:
    return get_chat_service(configs)


ChatDep = Annotated[
    ChatService,
    Depends(chat_dep)
]

def reranker_dep(
    configs: ConfigsDep
) -> ReRankerService:
    return get_rerank_service(configs)

ReRankerDep = Annotated[
    ReRankerService,
    Depends(reranker_dep)
]

def retrieval_dep(
    embed_service: EmbeddingDep,
    vecdb_service: VecDBDep,
    reranker_service: ReRankerDep
) -> RetrievalService:
    return get_retrieval_service(
        embed_service=embed_service,
        vecdb_service=vecdb_service,
        reranker_service=reranker_service
    )


RetrievalDep = Annotated[
    RetrievalService,
    Depends(retrieval_dep),
]

def qna_dep(
    chat_service: ChatDep
) -> QnAService:
    return get_qna_service(chat_service)


QnADep = Annotated[
    QnAService,
    Depends(qna_dep),
]

def praser_dep(
    configs: ConfigsDep
) -> ParserService:
    return get_parser_service(configs)

ParserDep = Annotated[
    ParserService,
    Depends(praser_dep),
]

async def temporal_client_dep(
    configs: ConfigsDep
) -> Client:
    return await get_temporal_client(configs)

TemporalClientDep = Annotated[
    Client,
    Depends(temporal_client_dep),
]