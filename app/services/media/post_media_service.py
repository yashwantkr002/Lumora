"""
===========================================================
File: app/services/media/post_media_service.py
===========================================================

PURPOSE

Post media management service.

Responsibilities

• Upload single image
• Upload multiple images
• Replace media
• Delete media

Future

• Video Upload
• Mixed Media
• Carousel
• Stories
• Reels

===========================================================
"""

from __future__ import annotations

import logging

from django.core.files.uploadedfile import UploadedFile

from app.core.storage.types import StoredFile
from app.services.media.image_service import ImageService
from app.services.media.upload_service import UploadService
from app.services.media.validators.post_media import (
    validate_post_image,
    validate_post_media,
)

logger = logging.getLogger(__name__)


class PostMediaService:
    """
    Service responsible for post media management.
    """

    POST_FOLDER = "posts"

    def __init__(self) -> None:

        self.image_service = ImageService()

        self.upload_service = UploadService()

    # -----------------------------------------------------
    # Upload Single Image
    # -----------------------------------------------------

    def upload_image(
        self,
        *,
        file: UploadedFile,
    ) -> StoredFile:
        """
        Upload a single post image.
        """

        validate_post_image(
            file=file,
        )

        optimized = self.image_service.optimize(
            file=file,
        )

        stored = self.upload_service.upload(
            file=optimized,
            folder=self.POST_FOLDER,
        )

        logger.info(
            "Post image uploaded.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Upload Multiple Images
    # -----------------------------------------------------

    def upload_images(
        self,
        *,
        files: list[UploadedFile],
    ) -> list[StoredFile]:
        """
        Upload multiple post images.
        """

        validate_post_media(
            files=files,
        )

        uploaded_files: list[StoredFile] = []

        for file in files:

            optimized = self.image_service.optimize(
                file=file,
            )

            stored = self.upload_service.upload(
                file=optimized,
                folder=self.POST_FOLDER,
            )

            uploaded_files.append(stored)

        logger.info(
            "Multiple post images uploaded.",
            extra={
                "count": len(uploaded_files),
            },
        )

        return uploaded_files

    # -----------------------------------------------------
    # Replace Image
    # -----------------------------------------------------

    def replace_image(
        self,
        *,
        old_image: str | None,
        new_image: UploadedFile,
    ) -> StoredFile:
        """
        Replace an existing post image.
        """

        validate_post_image(
            file=new_image,
        )

        optimized = self.image_service.optimize(
            file=new_image,
        )

        stored = self.upload_service.replace(
            old_file_path=old_image,
            new_file=optimized,
            folder=self.POST_FOLDER,
        )

        logger.info(
            "Post image replaced.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Delete Image
    # -----------------------------------------------------

    def delete_image(
        self,
        *,
        image_path: str,
    ) -> None:
        """
        Delete a post image.
        """

        self.upload_service.delete(
            file_path=image_path,
        )

        logger.info(
            "Post image deleted.",
            extra={
                "path": image_path,
            },
        )