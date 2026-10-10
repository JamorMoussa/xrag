from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
from llama_index.core import Document as LlamaindexDocument
from llama_index.core.schema import TextNode

from .base import ChunkingStrategy
from xrag.models import Document, ChunkList, Chunk, ChunkMetadata
from xrag.configs import Configs


class MarkdownBasedChunking(ChunkingStrategy):

    def __init__(
        self,
        configs: Configs
    ):
        super().__init__(configs=configs)
        self.parser = MarkdownNodeParser.from_defaults(
            include_metadata=True,
            include_prev_next_rel=True,
        )

        # TODO: Make the chunk size and overlap size dynamic: make sure to update metadata as well.
        self.splitter = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
        )

    def chunk(
        self,
        docs: list[Document],
        metadata: dict
    ) -> ChunkList:
        
        llamaindex_documents = [
                LlamaindexDocument(
                    text=page.content,
                    metadata={
                        **metadata, "page": page.page
                    },
                )
                for page in docs.pages
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
                        **metadata,
                        page=node.metadata["page"],
                        chunk_size=512,
                        chunk_overlap=50,
                        embedding_model=self.configs.EMBEDDING_MODEL,
                        embedding_provider=self.configs.EMBEDDING_PROVIDER
                    )
                )
                for node in nodes
            ]
        )

        return chunk_list