from xrag.configs import Configs
from xrag.models import AugmentedQuery
from .llms import OpenAIChatService

class QnAService:

    def __init__(
        self, 
        configs: Configs
    ):
        self.chat_service = OpenAIChatService(configs=configs)

    async def ask(
        self, 
        query: AugmentedQuery 
    ) -> str:
        return await self.chat_service.ask(
            query=query
        )