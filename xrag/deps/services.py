from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.client import Client

from xrag.configs import Configs
from xrag.services.storage import StorageService, S3StorageService
from xrag.services.embed import EmbeddingService, OpenAIEmbeddingService
from xrag.services.vecdb import VecDBService, QdrantVecDBService
from xrag.services.ingest.parse import ParserService, LiteParserService
from xrag.services.retrieve import RetrievalService, ReRankerService
from xrag.services.qna.llms import ChatService, OpenAIChatService
from xrag.services.qna import QnAService


def get_storage_service(
    configs: Configs,
) -> StorageService:
    return S3StorageService(
        configs=configs,
    )


def get_embed_service(
    configs: Configs,
) -> EmbeddingService:
    return OpenAIEmbeddingService(
        configs=configs,
    )


def get_vecdb_service(
    configs: Configs,
) -> VecDBService:
    return QdrantVecDBService(
        configs=configs,
    )


def get_parser_service(
    configs: Configs,
) -> ParserService:
    return LiteParserService(
        configs=configs,
    )

def get_rerank_service(
    configs: Configs
) -> ReRankerService:
    return ReRankerService(
        configs=configs
    )

def get_retrieval_service(
    embed_service: EmbeddingService,
    vecdb_service: VecDBService,
    reranker_service: ReRankerService
) -> RetrievalService:
    return RetrievalService(
        embed_service=embed_service,
        vecdb_service=vecdb_service,
        reranker_service=reranker_service
    )

def get_chat_service(
    configs: Configs
) -> ChatService:
    return OpenAIChatService(configs)

def get_qna_service(
    chat_service: ChatService
) -> QnAService:
    return QnAService(chat_service=chat_service)

async def get_temporal_client(
    configs: Configs
) -> Client:
    return await Client.connect(
        configs.TEMPORAL_HOST,
        namespace=configs.TEMPORAL_NAMESPACE,
        data_converter=pydantic_data_converter,
    )