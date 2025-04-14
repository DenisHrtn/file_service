from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, UploadFile, status

from application.enums.file_type import FileTypeEnum
from application.interactors.file_manager_interactor import FileManager
from containers import Container


router = APIRouter(tags=['files'])


@router.post('/upload')
@inject
async def upload_file(
        entity: str,
        file_type: FileTypeEnum = FileTypeEnum.TASKS,
        file: UploadFile = File(...),
        file_manager: FileManager = Depends(
            Provide[Container.file_manager_use_case]
        )
):
    response = await file_manager.upload(file, file_type, entity)
    return {'url': response}


@router.get('/filename', status_code=status.HTTP_200_OK)
@inject
async def get_filename(
        filename: str,
        file_manager: FileManager = Depends(
            Provide[Container.file_manager_use_case]
        )
):
    response = await file_manager.get(filename)
    return {'url': response}


@router.put('/update')
@inject
async def upload_file(
        filename: str,
        file: UploadFile = File(...),
        file_manager: FileManager = Depends(
            Provide[Container.file_manager_use_case]
        )
):
    response = await file_manager.update(file, filename)
    return {'url': response}


@router.delete("/filename", status_code=status.HTTP_200_OK)
@inject
async def delete_image(
    filename: str,
    file_manager: FileManager = Depends(
        Provide[Container.delete_file_usecase]
    ),
):
    file = await file_manager.delete(filename)
    return {"delete": file}
