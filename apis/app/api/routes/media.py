from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/{image_path}")
@inject
async def media_file(image_path: str):
    return FileResponse('/media/' + image_path)
