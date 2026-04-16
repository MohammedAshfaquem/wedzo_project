from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import List
from backend import schemas, models
from backend.auth import get_current_admin
from backend.cloudinary_utils import upload_image, upload_audio
from backend.removebg import remove_background

router = APIRouter(prefix="/api/media", tags=["media"])


@router.post("/upload/photo", response_model=schemas.PhotoUploadResponse)
async def upload_photo(
    file: UploadFile = File(...),
    _: models.Admin = Depends(get_current_admin),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    original_url = await upload_image(file, folder="weddings/photos")
    cutout_url = await remove_background(original_url)

    return {"original_url": original_url, "cutout_url": cutout_url}


@router.post("/upload/gallery", response_model=List[schemas.MediaUploadResponse])
async def upload_gallery(
    files: List[UploadFile] = File(...),
    _: models.Admin = Depends(get_current_admin),
):
    if len(files) > 8:
        raise HTTPException(status_code=400, detail="Maximum 8 gallery photos allowed")

    urls = []
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"File {file.filename} must be an image")
        url = await upload_image(file, folder="weddings/gallery")
        urls.append({"url": url})

    return urls


@router.post("/upload/music", response_model=schemas.MediaUploadResponse)
async def upload_music(
    file: UploadFile = File(...),
    _: models.Admin = Depends(get_current_admin),
):
    allowed_types = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File must be an audio file (mp3, wav, ogg)")

    url = await upload_audio(file, folder="weddings/music")
    return {"url": url}
