import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


async def upload_image(file: UploadFile, folder: str = "weddings/photos") -> str:
    try:
        contents = await file.read()
        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="image",
        )
        return result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")


async def upload_audio(file: UploadFile, folder: str = "weddings/music") -> str:
    try:
        contents = await file.read()
        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="video",  # Cloudinary uses 'video' for audio
        )
        return result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio upload failed: {str(e)}")


async def upload_image_bytes(image_bytes: bytes, folder: str = "weddings/cutouts") -> str:
    try:
        result = cloudinary.uploader.upload(
            image_bytes,
            folder=folder,
            resource_type="image",
        )
        return result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cutout upload failed: {str(e)}")


def delete_file(public_id: str) -> None:
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass  # Best effort deletion
