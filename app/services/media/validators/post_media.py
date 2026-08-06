"""
===========================================================
File: app/services/media/validators/post_media.py
===========================================================

PURPOSE

Post media validation.

Business Rules

• Maximum 10 files
• Images only (currently)
• Maximum Size: 10 MB per image
• Minimum Resolution: 300 × 300
• RGB / RGBA
• JPEG / PNG / WEBP

Future

• Mixed Media
• Videos
• Carousel
• Reels

===========================================================
"""

from __future__ import annotations

from typing import Iterable

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from app.services.media.exceptions import (
    InvalidMediaCount,
)

from .image import validate_image

# -------------------------------------------------------
# Constants
# -------------------------------------------------------

POST_MAX_MEDIA_COUNT = getattr(
    settings,
    "MEDIA_POST_MAX_FILES",
    10,
)

POST_MAX_SIZE = getattr(
    settings,
    "MEDIA_MAX_POST_SIZE",
    10 * 1024 * 1024,
)

# -------------------------------------------------------
# Single Media Validation
# -------------------------------------------------------

def validate_post_image(
    *,
    file: UploadedFile,
) -> None:
    """
    Validate a single post image.
    """

    validate_image(
        file=file,
        max_size=POST_MAX_SIZE,
    )

# -------------------------------------------------------
# Multiple Media Validation
# -------------------------------------------------------

def validate_post_media(
    *,
    files: Iterable[UploadedFile],
) -> None:
    """
    Validate post media collection.
    """

    files = list(files)

    if not files:

        raise InvalidMediaCount(
            "At least one media file is required."
        )

    if len(files) > POST_MAX_MEDIA_COUNT:

        raise InvalidMediaCount(
            f"Maximum {POST_MAX_MEDIA_COUNT} media files are allowed."
        )

    for file in files:

        validate_post_image(
            file=file,
        )