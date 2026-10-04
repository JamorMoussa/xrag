from temporalio import activity
from llama_index.core.node_parser  import MarkdownNodeParser, SentenceSplitter
from llama_index.core import Document as LlamaindexDocument
from llama_index.core.schema import TextNode
import json 

from xrag.configs import Configs
from xrag.api.schemas import IngestArgs
from xrag.services.storage import (
    S3StorageService, PathObject, FileObject
)
from xrag.models import Document, ChunkList, Chunk, ChunkMetadata
from xrag.services.ingest.parse import LiteParserService
from xrag.services.embed import OpenAIEmbeddingService
from xrag.services.vecdb import QdrantVecDBService


class ParsingActivity:

    def __init__(
        self, 
        configs: Configs
    ):
        self.configs = configs

        self.storage_service = S3StorageService(
            configs=configs
        )

        self.parser = LiteParserService(
            configs=configs
        )

    @activity.defn
    async def parse(
        self,
        args: IngestArgs
    ) -> IngestArgs:

        path_parsed = PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id,
                document_type="parsed"
        )

        file: FileObject = self.storage_service.load(
            path=PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id
            )
        )

        document = await self.parser.parse(
            content=file.content,
            filename=file.filename,
            content_type=file.content_type,
        )

        self.storage_service.save(
            file=FileObject(
                content=document.model_dump_json().encode("utf-8"),
                filename="parsed.json",
                content_type="application/json"
            ),
            path=path_parsed
        )

        return args.model_copy(
            update={
                "parsed_key": path_parsed.key 
            }
        )


class ChunkingActivity:


    def __init__(
        self, 
        configs: Configs,
    ):
        self.storage_service = S3StorageService(
            configs=configs
        )

        self.parser = MarkdownNodeParser.from_defaults(
            include_metadata=True,
            include_prev_next_rel=True,
        )

        # TODO: Make the chunk size and overlap size dynamic: make sure to update metadata as well.
        self.splitter = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
        )

    def normalize_nodes(
        self,
        nodes: list[TextNode],
        min_chars: int = 100,
    ) -> list[TextNode]:

        result: list[TextNode] = []
        buffer = ""

        for node in nodes:
            text = node.text.strip()

            is_heading = (
                text.startswith("#")
                and "\n" not in text
            )

            if is_heading:
                buffer = text
                continue

            if buffer:
                text = f"{buffer}\n\n{text}"
                buffer = ""

            if len(text) < min_chars and result:
                result[-1].text = (
                    result[-1].text.rstrip()
                    + "\n\n"
                    + text
                )
                continue

            node.text = text
            result.append(node)

        return result

    @activity.defn
    async def chunk(
        self,
        args: IngestArgs
    ) -> dict:

        file: FileObject = self.storage_service.load(
            path=PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id,
                document_type="parsed"
            )
        )

        document = Document(**json.loads(file.content))

        llamaindex_documents = [
                LlamaindexDocument(
                    text=page.content,
                    metadata={
                        "workspace_id":args.workspace_id, "document_id": args.document_id, "page": page.page
                    },
                )
                for page in document.pages
        ]

        sections = (
            self.parser.get_nodes_from_documents(
                documents=llamaindex_documents
            )
        )

        sections = self.normalize_nodes(
            sections
        )

        nodes: list[TextNode] = self.splitter(sections)

        chunk_list = ChunkList(
            chunks= [
                Chunk(
                    id_=node.id_,
                    text=node.text,
                    metadata=ChunkMetadata(
                        chunk_id=node.id_,
                        workspace_id=args.workspace_id,
                        document_id=args.document_id,
                        page=node.metadata["page"],
                        chunk_size=512,
                        chunk_overlap=50
                    )
                )
                for node in nodes
            ]
        )

        self.storage_service.save(
            file=FileObject(
                content=chunk_list.model_dump_json().encode("utf-8"),
                filename="chunks.json",
                content_type="application/json"
            ),
            path=PathObject(
                workspace_id=args.workspace_id, document_id=args.document_id, document_type="chunks"
            )
        )

        return {
            "chunks_key": PathObject(
                workspace_id=args.workspace_id, document_id=args.document_id, document_type="chunks"
            ).key
        }


class EmbeddingActivity:

    def __init__(
        self, 
        configs: Configs,
    ):
        self.storage_service = S3StorageService(
            configs=configs
        )

        self.embed_service = OpenAIEmbeddingService(
            configs=configs
        )

        self.vecdb_service = QdrantVecDBService(
            configs=configs
        )

    @activity.defn
    async def embed(
        self, 
        args: IngestArgs
    ) -> IngestArgs:

        batch_size: int = 32

        file: FileObject = self.storage_service.load(
            path=PathObject(
                workspace_id=args.workspace_id,
                document_id=args.document_id,
                document_type="chunks"
            )
        )

        chunks = ChunkList.model_validate_json(
            file.content
        ).chunks

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            await self.embed_upsert(
                chunks=batch
            )

        return args

    async def embed_upsert(
        self, 
        chunks: list[Chunk]
    ):
        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = await self.embed_service.embed(
            texts=texts
        )

        await self.vecdb_service.upsert(
            chunks=chunks, embeddings=embeddings
        )
