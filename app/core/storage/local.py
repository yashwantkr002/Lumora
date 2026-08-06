"""
===========================================================
File: app/core/storage/local.py
===========================================================

PURPOSE

Local filesystem storage implementation.

Implements BaseStorage.

Used for:

• Development
• Local testing
• Fallback storage

===========================================================
"""

from __future__ import annotations

import logging
import os
import uuid

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile

from .base import BaseStorage
from .types import StoredFile

logger = logging.getLogger(__name__)


class LocalStorage(BaseStorage):
    """
    Local storage backend.
    """

    def upload(
        self,
        *,
        file: UploadedFile,
        folder: str,
    ) -> str:

        resolved_folder = self.resolve_folder(folder)

        filename = self._generate_filename(
            file=file,
            folder=resolved_folder,
        )

        saved_path = default_storage.save(
            filename,
            file,
        )

        logger.info(
            "File uploaded.",
            extra={
                "path": saved_path,
                "provider": "local",
            },
        )

        return StoredFile(
            provider="local",
            path=saved_path,
            url=default_storage.url(saved_path),
            filename=os.path.basename(saved_path),
            content_type=getattr(file, "content_type", None),
            size=getattr(file, "size", None),
        )

    def delete(
        self,
        *,
        file_path: str,
    ) -> None:

        if default_storage.exists(file_path):

            default_storage.delete(file_path)

            logger.info(
                "File deleted.",
                extra={
                    "path": file_path,
                },
            )

    def exists(
        self,
        *,
        file_path: str,
    ) -> bool:

        return default_storage.exists(file_path)

    def url(
        self,
        *,
        file_path: str,
    ) -> str:

        return default_storage.url(file_path)

    def metadata(
        self,
        *,
        file_path: str,
    ) -> StoredFile:
        return StoredFile(
            provider="local",
            path=file_path,
            url=self.url(file_path=file_path),
            filename=os.path.basename(file_path),
            content_type=None,
            size=None,
            width=None,
            height=None,
            public_id=file_path,
            version=None,
            format=None,
        )

    # -----------------------------------------------------
    # Helpers
    # -----------------------------------------------------

    @staticmethod
    def _generate_filename(
        *,
        file: UploadedFile,
        folder: str,
    ) -> str:

        extension = os.path.splitext(
            file.name,
        )[1].lower()

        unique_name = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        folder = folder.strip("/")

        return (
            f"{folder}/"
            f"{unique_name}"
        )