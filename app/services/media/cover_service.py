"""
===========================================================
File: app/services/media/cover_service.py
===========================================================

PURPOSE

Cover image management service.

Responsibilities

• Validate cover image
• Optimize cover image
• Upload cover image
• Replace cover image
• Delete cover image

===========================================================
"""

from __future__ import annotations

import logging

from django.core.files.uploadedfile import UploadedFile

from app.core.storage.types import StoredFile
from app.services.media.image_service import ImageService
from app.services.media.upload_service import UploadService
from app.services.media.validators.cover import validate_cover

logger = logging.getLogger(__name__)


class CoverService:
    """
    Cover image management service.
    """

    COVER_FOLDER = "covers"

    def __init__(self) -> None:

        self.image_service = ImageService()

        self.upload_service = UploadService()

    # -----------------------------------------------------
    # Upload Cover
    # -----------------------------------------------------

    def upload_cover(
        self,
        *,
        file: UploadedFile,
    ) -> StoredFile:
        """
        Upload a new cover image.
        """

        validate_cover(
            file=file,
        )

        optimized = self.image_service.optimize(
            file=file,
        )

        stored = self.upload_service.upload(
            file=optimized,
            folder=self.COVER_FOLDER,
        )

        logger.info(
            "Cover uploaded.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Replace Cover
    # -----------------------------------------------------

    def replace_cover(
        self,
        *,
        old_cover: str | None,
        new_cover: UploadedFile,
    ) -> StoredFile:
        """
        Replace an existing cover image.
        """

        validate_cover(
            file=new_cover,
        )

        optimized = self.image_service.optimize(
            file=new_cover,
        )

        stored = self.upload_service.replace(
            old_file_path=old_cover,
            new_file=optimized,
            folder=self.COVER_FOLDER,
        )

        logger.info(
            "Cover replaced.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Delete Cover
    # -----------------------------------------------------

    def delete_cover(
        self,
        *,
        cover_path: str,
    ) -> None:
        """
        Delete cover image.
        """

        self.upload_service.delete(
            file_path=cover_path,
        )

        logger.info(
            "Cover deleted.",
            extra={
                "path": cover_path,
            },
        )