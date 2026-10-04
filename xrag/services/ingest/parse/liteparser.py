import httpx
import json

from .base import ParserService
from xrag.configs import Configs
from xrag.models import Document, Page



class LiteParserService(ParserService):

    def __init__(
        self, configs: Configs
    ):
        super().__init__(configs=configs)

        self.client = httpx.AsyncClient(
            base_url=self.configs.LITE_PARSER_BASE_URL,
            timeout=120.0
        )

    async def parse(
        self,
        content: bytes,
        filename: str,
        content_type: str,
    ) -> Document:
        
        config = {
            "outputFormat": "markdown",
            "imageMode": "placeholder",
            "extractLinks": True,
        }

        response = await self.client.post(
            "/parse",
            files={
                "file": (filename, content, content_type),
            },
            data={
                "config": json.dumps(config)
            },
        )

        response.raise_for_status()

        result = response.json()

        return Document(
            pages=[
                Page(
                    page=page["pageNum"], 
                    content=page["markdown"]
                ) for page in result["pages"]
            ]
        )
    
    async def close(self):
        await self.client.aclose()
        