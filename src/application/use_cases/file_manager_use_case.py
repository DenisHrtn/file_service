from abc import ABC, abstractmethod

from application.interfaces.get_content_type import IGetContentType
from application.interfaces.minio_interface import IMinioService


class FileManagerUseCase(ABC):
    def __init__(
        self,
        minio_service: IMinioService,
        content_type: IGetContentType,
    ):
        self.minio_service = minio_service
        self.content_type = content_type

    @abstractmethod
    async def get(self, filename: str) -> str:
        pass

    @abstractmethod
    async def upload(self, file, file_type: str, entity: str) -> str:
        pass

    @abstractmethod
    async def update(self, file, filename: str) -> str:
        pass

    @abstractmethod
    async def delete(self, filename: str) -> str:
        pass

    @abstractmethod
    async def parse(self, filename: str):
        pass

    @abstractmethod
    async def generate_unique_name(self, entity: str, media_index: str) -> str:
        pass
