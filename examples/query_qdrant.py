import asyncio

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
)

from xrag.configs import Configs
from xrag.services.embed import OpenAIEmbeddingService
from xrag.services.vecdb import QdrantVecDBService


async def main():
    configs = Configs()

    embed_service = OpenAIEmbeddingService(
        configs=configs
    )

    vecdb_service = QdrantVecDBService(
        configs=configs
    )

    query = "how to install llama-index"

    document_id = "4bbc13ed1cc94ad3b1aa4c8617211073"

    embedding = await embed_service.embed(
        texts=query
    )

    results = await vecdb_service.client.query_points(
        collection_name="xrag",
        query=embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchAny(
                        any=[
                            document_id
                        ]
                    ),
                )
            ]
        ),
        limit=10,
        with_payload=True,
        with_vectors=False,
    )

    print(f"\nQuery: {query}")
    print(f"Document ID: {document_id}")
    print(f"Results: {len(results.points)}\n")

    for index, point in enumerate(
        results.points,
        start=1
    ):
        print(f"--- Result {index} ---")
        print(f"Score: {point.score}")
        print(f"ID: {point.id}")

        payload = point.payload or {}

        print(f"Page: {payload.get('page')}")
        print(f"Document: {payload.get('document_id')}")
        print(f"Text:\n{payload.get('text')}")
        print()


if __name__ == "__main__":
    asyncio.run(main())