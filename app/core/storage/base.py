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
from .types import StoredFile
from django.core.files.uploadedfile import UploadedFile


class BaseStorage(ABC):
    """
    Storage backend contract.
    """


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
