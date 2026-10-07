from xrag.models import AugmentedQuery
from .llms import ChatService

class QnAService:

    def __init__(
        self, 
        chat_service: ChatService
    ):
        self.chat_service = chat_service

    async def ask(
        self, 
        query: AugmentedQuery 
    ) -> str:
        return (
            await self.chat_service.ask(
                query=query
            )
        )