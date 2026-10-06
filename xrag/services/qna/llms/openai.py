from openai import AsyncOpenAI

from .base import ChatService
from xrag.models import AugmentedQuery
from xrag.configs import Configs

class OpenAIChatService(ChatService):

    def __init__(
        self,
        configs: Configs 
    ):
        self.configs = configs

        self.client = AsyncOpenAI(
            base_url=self.configs.CHAT_MODEL_BASE_URL,
            api_key=self.configs.CHAT_MODEL_API_KEY
        )

    async def ask(
        self,
        query: AugmentedQuery
    ) -> str:
        response = await self.client.responses.create(
            model=self.configs.CHAT_MODEL_NAME,
            instructions=query.instructions,
            input=query.input
        )

        return response.output_text