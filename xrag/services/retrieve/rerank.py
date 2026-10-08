import httpx

from xrag.models import RetrievedSnippet
from xrag.configs import Configs

class ReRankerService:

    def __init__(
        self, 
        configs: Configs
    ):
        self.configs = configs 
        self.client = httpx.AsyncClient(
            base_url=self.configs.LLAMA_CPP_BASE_URL
        )

    async def rerank(
        self,
        query: str,
        snippets: list[RetrievedSnippet], 
        top_k: int
    ):
        snippets_dict = {
            i: snippet for i, snippet in enumerate(snippets)
        }

        response = await self.client.post(
            "/rerank",
            json={
                "model": self.configs.RERANK_MODEL_NAME,
                "query": query,
                "top_n": top_k,
                "documents": [
                    snippet.text for snippet in snippets
                ]
            }
        )

        response.raise_for_status()

        results = sorted(
            response.json()["results"],
            key = lambda r: r["relevance_score"],
            reverse=True
        )

        indexes = list(map(lambda r: r["index"], results))

        return [
            snippets_dict[i] for i in indexes
        ]

