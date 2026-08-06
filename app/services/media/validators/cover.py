"""
===========================================================
File: app/services/media/validators/cover.py
===========================================================

PURPOSE

Cover image validation.

Business Rules

• Maximum Size: 10 MB
• Minimum Resolution: 1200 × 400
• Landscape Image
• Aspect Ratio:
    • 16:9
    • 3:1
• RGB / RGBA
• JPEG / PNG / WEBP

===========================================================
"""

from __future__ import annotations

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .image import (
    validate_aspect_ratio,
    validate_image,
    validate_image_dimensions,
    validate_image_integrity,
)

# -------------------------------------------------------
# Constants
# -------------------------------------------------------

COVER_MAX_SIZE = getattr(
    settings,
    "MEDIA_MAX_COVER_SIZE",
    10 * 1024 * 1024,
)

MIN_WIDTH = getattr(
    settings,
    "MEDIA_MIN_COVER_WIDTH",
    1200,
)

MIN_HEIGHT = getattr(
    settings,
    "MEDIA_MIN_COVER_HEIGHT",
    400,
)

ALLOWED_ASPECT_RATIOS = {
    (16, 9),
    (3, 1),
}

# -------------------------------------------------------
# Cover Validation
# -------------------------------------------------------

def validate_cover(
    *,
    file: UploadedFile,
) -> None:
    """
    Validate cover image.
    """

    validate_image(
        file=file,
        max_size=COVER_MAX_SIZE,
    )

    image = validate_image_integrity(
        file=file,
    )

    validate_image_dimensions(
        image=image,
    )

    width, height = image.size

    if width < MIN_WIDTH or height < MIN_HEIGHT:

        raise InvalidImageDimensions()

    if width <= height:

        raise InvalidImageDimensions(
            "Cover image must be landscape."
        )

    validate_aspect_ratio(
        image=image,
        allowed=ALLOWED_ASPECT_RATIOS,
    )