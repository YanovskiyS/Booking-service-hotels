from fastapi import APIRouter, UploadFile

from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile):
    ImageService().upload_image(file)
