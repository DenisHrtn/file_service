from abc import ABC, abstractmethod


class IGetContentType(ABC):
    @abstractmethod
    async def get_content_type(self, content: str) -> str:
        pass
