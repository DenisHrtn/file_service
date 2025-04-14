from abc import ABC, abstractmethod


class IMinioService(ABC):
    @abstractmethod
    async def upload_file(
        self, file, filename: str, content_type: str, bucket_name: str
    ):
        pass

    @abstractmethod
    async def get_file_url(self, filename: str, bucket_type: str) -> str:
        pass

    @abstractmethod
    async def update_file(
        self, file, filename: str, content_type: str, bucket_type: str
    ):
        pass

    @abstractmethod
    async def delete_file(self, filename: str, bucket_type: str):
        pass

    @abstractmethod
    async def file_exists(self, filename: str, bucket_type: str) -> bool:
        pass

    @abstractmethod
    async def get_last_index(self, prefix: str, bucket_type: str) -> int:
        pass
