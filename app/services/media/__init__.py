from app.services.media.upload_service import UploadService

try:
    from .media_service import MediaService
except ModuleNotFoundError:  # pragma: no cover
    from .compat_media_service import MediaService

__all__ = ["MediaService", "UploadService"]
