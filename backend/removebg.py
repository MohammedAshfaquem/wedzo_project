import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
from backend.cloudinary_utils import upload_image_bytes

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)

REMOVEBG_API_KEY = os.getenv("REMOVEBG_API_KEY", "")
REMOVEBG_API_URL = "https://api.remove.bg/v1.0/removebg"


async def remove_background(image_url: str) -> str:
    """
    Calls remove.bg API with an image URL, uploads the result to Cloudinary,
    and returns the Cloudinary URL of the cutout PNG.
    """
    if not REMOVEBG_API_KEY:
        return image_url  # Fall back to original if no API key

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                REMOVEBG_API_URL,
                headers={"X-Api-Key": REMOVEBG_API_KEY},
                data={
                    "image_url": image_url,
                    "size": "auto",
                    "format": "png",
                },
            )

        if response.status_code == 200:
            cutout_bytes = response.content
            cutout_url = await upload_image_bytes(cutout_bytes, folder="weddings/cutouts")
            return cutout_url
        else:
            # If remove.bg fails, return original
            return image_url

    except Exception:
        return image_url  # Graceful fallback
