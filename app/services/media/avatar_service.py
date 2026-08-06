"""
===========================================================
File: app/services/media/avatar_service.py
===========================================================

PURPOSE

Avatar management service.

Responsibilities

• Validate avatar
• Optimize avatar
• Upload avatar
• Replace avatar
• Delete avatar

===========================================================
"""

from __future__ import annotations

import logging

from django.core.files.uploadedfile import UploadedFile

from app.core.storage.types import StoredFile
from app.services.media.image_service import ImageService
from app.services.media.upload_service import UploadService
from app.services.media.validators.avatar import validate_avatar

logger = logging.getLogger(__name__)


class AvatarService:
    """
    Avatar upload service.
    """

    AVATAR_FOLDER = "avatars"

    def __init__(self) -> None:

        self.image_service = ImageService()

        self.upload_service = UploadService()

    # -----------------------------------------------------
    # Upload Avatar
    # -----------------------------------------------------

    def upload_avatar(
        self,
        *,
        file: UploadedFile,
    ) -> StoredFile:
        """
        Upload new avatar.
        """

        validate_avatar(
            file=file,
        )

        optimized = self.image_service.optimize(
            file=file,
        )

        stored = self.upload_service.upload(
            file=optimized,
            folder=self.AVATAR_FOLDER,
        )

        logger.info(
            "Avatar uploaded.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Replace Avatar
    # -----------------------------------------------------

    def replace_avatar(
        self,
        *,
        old_avatar: str | None,
        new_avatar: UploadedFile,
    ) -> StoredFile:
        """
        Replace existing avatar.
        """

        validate_avatar(
            file=new_avatar,
        )

        optimized = self.image_service.optimize(
            file=new_avatar,
        )

        stored = self.upload_service.replace(
            old_file_path=old_avatar,
            new_file=optimized,
            folder=self.AVATAR_FOLDER,
        )

        logger.info(
            "Avatar replaced.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Delete Avatar
    # -----------------------------------------------------

    def delete_avatar(
        self,
        *,
        avatar_path: str,
    ) -> None:
        """
        Delete avatar.
        """

        self.upload_service.delete(
            file_path=avatar_path,
        )

        logger.info(
            "Avatar deleted.",
            extra={
                "path": avatar_path,
            },
        )