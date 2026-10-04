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
from xrag.services.ingestion.parse import LiteParserService


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