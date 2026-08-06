"""
===========================================================
File: app/services/media/video_service.py
===========================================================

PURPOSE

Video management service.

Responsibilities

• Validate videos
• Upload videos
• Replace videos
• Delete videos

Future

• FFmpeg Processing
• Thumbnail Generation
• Video Compression
• Adaptive Streaming
• HLS Conversion

===========================================================
"""

from __future__ import annotations

import logging

from django.core.files.uploadedfile import UploadedFile

from app.core.storage.types import StoredFile
from app.services.media.upload_service import UploadService
from app.services.media.validators.video import validate_video

logger = logging.getLogger(__name__)


class VideoService:
    """
    Video upload and management service.
    """

    VIDEO_FOLDER = "videos"

    def __init__(self) -> None:

        self.upload_service = UploadService()

    # -----------------------------------------------------
    # Upload Video
    # -----------------------------------------------------

    def upload_video(
        self,
        *,
        file: UploadedFile,
    ) -> StoredFile:
        """
        Upload a new video.
        """

        validate_video(
            file=file,
        )

        stored = self.upload_service.upload(
            file=file,
            folder=self.VIDEO_FOLDER,
        )

        logger.info(
            "Video uploaded.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Replace Video
    # -----------------------------------------------------

    def replace_video(
        self,
        *,
        old_video: str | None,
        new_video: UploadedFile,
    ) -> StoredFile:
        """
        Replace an existing video.
        """

        validate_video(
            file=new_video,
        )

        stored = self.upload_service.replace(
            old_file_path=old_video,
            new_file=new_video,
            folder=self.VIDEO_FOLDER,
        )

        logger.info(
            "Video replaced.",
            extra={
                "path": stored.path,
            },
        )

        return stored

    # -----------------------------------------------------
    # Delete Video
    # -----------------------------------------------------

    def delete_video(
        self,
        *,
        video_path: str,
    ) -> None:
        """
        Delete a video.
        """

        self.upload_service.delete(
            file_path=video_path,
        )

        logger.info(
            "Video deleted.",
            extra={
                "path": video_path,
            },
        )

    # -----------------------------------------------------
    # Video URL
    # -----------------------------------------------------

    def get_video_url(
        self,
        *,
        video_path: str,
    ) -> str:
        """
        Return public video URL.
        """

        return self.upload_service.url(
            file_path=video_path,
        )