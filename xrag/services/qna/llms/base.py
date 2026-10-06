from abc import ABC, abstractmethod

from xrag.models import AugmentedQuery

class ChatService(ABC):

    @abstractmethod
    async def ask(
        self,
        query: AugmentedQuery
    ):
        ... 