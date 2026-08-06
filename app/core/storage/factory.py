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

        return storage_class()