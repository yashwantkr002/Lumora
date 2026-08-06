"""
===========================================================
File: app/core/storage/base.py
===========================================================

PURPOSE

Abstract storage interface.

Every storage backend must implement this contract.

Supported providers:

• Local Storage
• Cloudinary
• Amazon S3 (future)
• Azure Blob (future)

===========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .types import StoredFile


class BaseStorage(ABC):
    """
    Storage backend contract.
    """

    def resolve_folder(self, folder: str) -> str:
        """Resolve a configured upload path for a media category."""

        configured_paths = getattr(settings, "MEDIA_UPLOAD_PATHS", {})
        if isinstance(configured_paths, dict) and folder in configured_paths:
            return str(configured_paths[folder]).strip("/")

        return folder.strip("/")

    @abstractmethod
    def upload(
        self,
        *,
        file: UploadedFile,
        folder: str,
        ) -> StoredFile:
        """ Upload a file. Returns ------- StoredFile """

    @abstractmethod
    def delete(
        self,
        *,
        file_path: str,
    ) -> None:
        """
        Delete a file.
        """

        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        *,
        file_path: str,
    ) -> bool:
        """
        Check whether file exists.
        """

        raise NotImplementedError

    @abstractmethod
    def url(
        self,
        *,
        file_path: str,
    ) -> str:
        """
        Return public URL.
        """

        raise NotImplementedError

    @abstractmethod
    def metadata(self,*,file_path: str,) -> StoredFile:
       """ Return metadata for a stored file."""
