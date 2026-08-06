import cloudinary
import cloudinary.uploader
from django.conf import settings


class CloudinaryConfig:
    @staticmethod
    def configure():
        cloudinary.config(
            cloud_name=getattr(settings, "CLOUDINARY_CLOUD_NAME", None),
            api_key=getattr(settings, "CLOUDINARY_API_KEY", None),
            api_secret=getattr(settings, "CLOUDINARY_API_SECRET", None),
            secure=True,
        )


CloudinaryConfig.configure()
