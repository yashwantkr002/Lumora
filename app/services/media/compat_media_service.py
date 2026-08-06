"""
Compatibility adapter for older media imports.

This preserves the historic MediaService API while delegating to the
new UploadService implementation.
"""

from __future__ import annotations

from django.core.files.uploadedfile import UploadedFile

from app.services.media.upload_service import UploadService


class MediaService:
    """Backward-compatible wrapper for the newer upload service."""

    upload_service = UploadService()

    @classmethod
    def upload_to_field(cls, instance, field_name, file, *, folder="media"):
        stored = cls.upload_service.upload(file=file, folder=folder)
        setattr(instance, field_name, stored.path)
        return stored
