import cloudinary
import cloudinary.uploader
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

async def upload_image(file, folder: str = "drivo"):
    """
    Upload a file to Cloudinary and return the secure URL.
    """
    try:
        # result = cloudinary.uploader.upload(file, folder=folder)
        # Note: cloudinary.uploader.upload is blocking, but for now we'll use it.
        # In a high-traffic app, we should use a thread pool.
        result = cloudinary.uploader.upload(file, folder=folder)
        return result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Upload Error: {str(e)}")
        return None
