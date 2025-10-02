from application.enums.buckets import BucketTypeEnum
from application.enums.file_type import FileTypeEnum
from application.interfaces.get_content_type import IGetContentType
from application.interfaces.minio_interface import IMinioService
from application.use_cases.file_manager_use_case import FileManagerUseCase

from .exceptions import (
    EmptyFilenameException,
    EmptyFileTypeException,
    FileDoesNotExistException,
)


class FileManager(FileManagerUseCase):
    def __init__(self, minio_service: IMinioService, content_type: IGetContentType):
        super().__init__(minio_service, content_type)

    async def get(self, filename: str) -> str:
        if not filename:
            raise EmptyFilenameException()

        task_id, media_index = await self.parse(filename)

        if media_index is None:
            bucket_type = BucketTypeEnum.AVATARS
        else:
            bucket_type = BucketTypeEnum.TASKS

        file_exists = await self.minio_service.file_exists(
            filename=filename, bucket_type=bucket_type
        )

        if not file_exists:
            raise FileDoesNotExistException()

        return await self.minio_service.get_file_url(
            filename=filename, bucket_type=bucket_type
        )

    async def upload(self, file, file_type: str, entity: str) -> str:
        media_index = 0

        match file_type:
            case FileTypeEnum.AVATAR:
                bucket_type = BucketTypeEnum.AVATARS
            case FileTypeEnum.TASKS:
                bucket_type = BucketTypeEnum.TASKS
                media_index = await self.minio_service.get_last_index(
                    entity, bucket_type
                )
                media_index += 1
            case _:
                raise EmptyFileTypeException()

        content_type = await self.content_type.get_content_type(file.filename)
        filename = await self.generate_unique_name(entity, media_index)
        file_url = await self.minio_service.upload_file(
            file=file,
            filename=filename,
            content_type=content_type,
            bucket_name=bucket_type,
        )

        return file_url

    async def update(self, file, filename: str) -> str:
        if not filename:
            raise EmptyFilenameException()

        entity, media_index = await self.parse(filename)

        if media_index is None:
            bucket_type = BucketTypeEnum.AVATARS
            filename = f"{entity}"
        else:
            bucket_type = BucketTypeEnum.TASKS
            filename = f"{entity}/{filename}"
        content_type = await self.content_type.get_content_type(file.filename)
        file_exists = await self.minio_service.file_exists(
            filename=filename, bucket_type=bucket_type
        )

        if not file_exists:
            raise FileDoesNotExistException()

        file_url = await self.minio_service.update_file(
            file=file,
            filename=filename,
            content_type=content_type,
            bucket_type=bucket_type,
        )

        return file_url

    async def delete(self, filename: str) -> str:
        if not filename:
            raise EmptyFilenameException()

        task_id, media_index = await self.parse(filename)

        if media_index is None:
            bucket_type = BucketTypeEnum.AVATARS
        else:
            bucket_type = BucketTypeEnum.TASKS
        file_exists = await self.minio_service.file_exists(
            filename=filename, bucket_type=bucket_type
        )

        if not file_exists:
            raise FileDoesNotExistException()

        return await self.minio_service.delete_file(
            filename=filename, bucket_type=bucket_type
        )

    async def generate_unique_name(self, entity: str, media_index: str) -> str:
        if media_index:
            return f"{entity}/{media_index}"

        return f"{entity}"

    async def parse(self, filename: str):
        parts = filename.split("/")
        task_id = parts[0]
        media_index = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        return task_id, media_index
