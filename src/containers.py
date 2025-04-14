from dependency_injector import containers, providers

from application.interactors.file_manager_interactor import FileManager
from config import BaseConfig
from infra.services.content_type.get_content_type_service import GetContentTypeService
from infra.services.minio.minio_service import MinioService


class Container(containers.DeclarativeContainer):
    config = providers.Factory(BaseConfig)

    aws_service = providers.Factory(MinioService, config=config.provided.AWS_CONFIG)
    content_type = providers.Factory(GetContentTypeService)

    file_manager_use_case = providers.Factory(
        FileManager, minio_service=aws_service, content_type=content_type
    )


container = Container()
container.init_resources()
