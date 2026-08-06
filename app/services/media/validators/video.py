"""
===========================================================
File: app/services/media/validators/video.py
===========================================================

PURPOSE

Production-grade video validation.

Supports

• MP4
• MOV
• WEBM

Future

• FFmpeg Validation
• Codec Validation
• Resolution Validation
• Thumbnail Generation
• Duration Validation

===========================================================
"""

from __future__ import annotations

from typing import Final

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from app.services.media.exceptions import (
    InvalidVideoFile,
)

from .common import (
    validate_extension,
    validate_file_size,
    validate_mime_type,
)

# -------------------------------------------------------
# Constants
# -------------------------------------------------------

SUPPORTED_EXTENSIONS: Final = {
    ".mp4",
    ".mov",
    ".webm",
}

SUPPORTED_MIME_TYPES: Final = {
    "video/mp4",
    "video/quicktime",
    "video/webm",
}

MAX_VIDEO_SIZE: Final = getattr(
    settings,
    "MEDIA_MAX_VIDEO_SIZE",
    200 * 1024 * 1024,
)

MAX_VIDEO_DURATION: Final = getattr(
    settings,
    "MEDIA_MAX_VIDEO_DURATION",
    300,
)

# -------------------------------------------------------
# Main Validator
# -------------------------------------------------------

def validate_video(
    *,
    file: UploadedFile,
) -> None:
    """
    Validate uploaded video.
    """

    validate_file_size(
        file=file,
        max_size=MAX_VIDEO_SIZE,
    )

    validate_extension(
        file=file,
        allowed_extensions=SUPPORTED_EXTENSIONS,
    )

    validate_mime_type(
        file=file,
        allowed_types=SUPPORTED_MIME_TYPES,
    )

    validate_video_integrity(
        file=file,
    )