from fastapi import APIRouter, File, UploadFile
import model.style_model as model
from PIL import Image
from fastapi.responses import StreamingResponse
from io import BytesIO


router = APIRouter(
    prefix='/model'
    )


@router.get('/')
async def root():
    """
    testing page
    :return: greetings
    """
    return {'massage': 'welcome to the deep learning model page'}


@router.post("/upload")
async def upload_file(content: UploadFile = File(...), style: UploadFile = File(...)):
    """
    get two images
    :param content:
    :param style:
    :return: styled image
    """
    extension = (content.filename.split(".")[-1] and style.filename.split(".")[-1]) in ("jpg", "jpeg", "png")

    if not extension:
        return "Image must be jpg or png format!"

    content_image = Image.open(content.file)
    style_image = Image.open(style.file)

    result_image = model.main(content_image, style_image)
    result = BytesIO()
    result_image.save(result, "JPEG")
    result.seek(0)

    return StreamingResponse(result, media_type="image/jpg")
