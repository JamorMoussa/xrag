import pytest

from xrag.configs import configs
from xrag.services.retrieve.rerank import ReRankerService
from xrag.models import RetrievedSnippet

configs.LLAMA_CPP_BASE_URL = "http://localhost:8080/"
reranker = ReRankerService(configs=configs)

texts = [
    "## 3 Experiments\n\nThe previously outlined framework is one possibility how different layers in transformers could communicate with each other and compute functions that ultimately lead to next token predictions.",
    "what the dataset used to train the gpt-2?"
]

@pytest.mark.asyncio
async def test_reranker():

    result = await reranker.rerank(
        query="what the dataset used to train the gpt-2?",
        snippets=[
            RetrievedSnippet(
                text=text, score=0.5, metadata={}
            )
            for text in texts
        ],
        top_k=5
    )

    assert isinstance(result[0], RetrievedSnippet)
    assert result[0].text == texts[1]