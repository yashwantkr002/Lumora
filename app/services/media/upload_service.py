"""
===========================================================
File: app/services/media/upload_service.py
===========================================================

PURPOSE

Central media upload service.

Responsibilities

• Upload files
• Delete files
• Replace files
• Return StoredFile object

This service is storage-provider agnostic.

===========================================================
"""

from __future__ import annotations

import logging

from django.core.files.uploadedfile import UploadedFile

from app.core.storage.factory import StorageFactory
from app.core.storage.types import StoredFile

logger = logging.getLogger(__name__)


class UploadService:
    """
    Generic media upload service.
    """

    def __init__(self) -> None:
        self.storage = StorageFactory.create()

    # -----------------------------------------------------
    # Upload
    # -----------------------------------------------------

    def upload(
        self,
        *,
        file: UploadedFile,
        folder: str,
    ) -> StoredFile:
        """
        Upload a single file.
        """

        stored_file = self.storage.upload(
            file=file,
            folder=folder,
        )

        logger.info(
            "Upload completed.",
            extra={
                "provider": stored_file.provider,
                "path": stored_file.path,
            },
        )

        return stored_file

    # -----------------------------------------------------
    # Delete
    # -----------------------------------------------------

    def delete(
        self,
        *,
        file_path: str,
    ) -> None:
        """
        Delete a stored file.
        """

        self.storage.delete(
            file_path=file_path,
        )

        logger.info(
            "File deleted.",
            extra={
                "path": file_path,
            },
        )

    # -----------------------------------------------------
    # Replace
    # -----------------------------------------------------

    def replace(
        self,
        *,
        old_file_path: str | None,
        new_file: UploadedFile,
        folder: str,
    ) -> StoredFile:
        """
        Replace an existing file.
        """

        if old_file_path:

            self.delete(
                file_path=old_file_path,
            )

        return self.upload(
            file=new_file,
            folder=folder,
        )

    # -----------------------------------------------------
    # Exists
    # -----------------------------------------------------

    def exists(
        self,
        *,
        file_path: str,
    ) -> bool:
        """
        Check whether file exists.
        """

        return self.storage.exists(
            file_path=file_path,
        )

    # -----------------------------------------------------
    # URL
    # -----------------------------------------------------

    def url(
        self,
        *,
        file_path: str,
    ) -> str:
        """
        Return public URL.
        """

        return self.storage.url(
            file_path=file_path,
        )