"""
===========================================================
File: app/core/storage/factory.py
===========================================================

PURPOSE

Storage Provider Factory.

Returns the configured storage backend.

Supported Providers

• Local Storage
• Cloudinary

Future

• Amazon S3
• Azure Blob

===========================================================
"""

from __future__ import annotations

from functools import lru_cache

from django.conf import settings

from .base import BaseStorage
from .cloudinary import CloudinaryStorage
from .local import LocalStorage


def _get_upload_path(folder: str) -> str:
    """Resolve a media folder path from settings with a fallback."""

    configured_paths = getattr(settings, "MEDIA_UPLOAD_PATHS", {})
    if isinstance(configured_paths, dict) and folder in configured_paths:
        return str(configured_paths[folder]).strip("/")

    return folder.strip("/")


class StorageFactory:
    """
    Resolve the configured storage backend.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def create() -> BaseStorage:
        """
        Return configured storage backend.
        """

        provider = getattr(
            settings,
            "MEDIA_STORAGE_PROVIDER",
            "local",
        ).lower()

        providers = {
            "local": LocalStorage,
            "cloudinary": CloudinaryStorage,
        }

        storage_class = providers.get(provider)

        if storage_class is None:
            raise ValueError(
                f"Unsupported storage provider: {provider}"
            )

        storage = storage_class()
        storage.upload_path_prefix = _get_upload_path
        return storage