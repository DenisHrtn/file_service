import aioboto3

from application.interfaces.minio_interface import IMinioService
from config import AWSConfig


class MinioService(IMinioService):
    def __init__(self, config: AWSConfig):
        self.session = aioboto3.Session()
        self.config = config

    async def upload_file(
            self,
            file,
            filename: str,
            content_type: str,
            bucket_name: str
    ):
        async with self.session.client(
            's3',
            endpoint_url=self.config.url,
            aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
        ) as s3_client:
            await s3_client.put_object(
                Bucket=bucket_name, Key=filename, Body=file, ContentType=content_type
            )

        return await self.get_file_url(filename, bucket_name)

    async def get_file_url(self, filename: str, bucket_name: str) -> str:
        return f"{self.config.local_url}/{bucket_name}/{filename}"

    async def update_file(
            self,
            file,
            filename: str,
            content_type: str,
            bucket_name: str
    ):
        return await self.upload_file(
            file=file,
            filename=filename,
            content_type=content_type,
            bucket_name=bucket_name
        )

    async def delete_file(self, filename: str, bucket_name: str):
        async with self.session.client(
                's3',
                endpoint_url=self.config.url,
                aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
        ) as s3_client:
            await s3_client.delete_object(Bucket=bucket_name, Key=filename)

        return True

    async def file_exists(self, filename: str, bucket_name: str):
        async with self.session.client(
                's3',
                endpoint_url=self.config.url,
                aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
        ) as s3_client:
            if await s3_client.head_object(Bucket=bucket_name, Key=filename):
                return True

            return False
