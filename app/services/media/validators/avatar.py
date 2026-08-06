"""
===========================================================
File: app/services/media/validators/avatar.py
===========================================================

PURPOSE

Avatar image validation.

Business Rules

• Maximum Size: 2 MB
• Minimum Resolution: 300 × 300
• Aspect Ratio: 1:1
• RGB / RGBA
• JPEG / PNG / WEBP

===========================================================
"""

from __future__ import annotations

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .image import (
    validate_image,
    validate_aspect_ratio,
    validate_image_integrity,
)

# -------------------------------------------------------
# Constants
# -------------------------------------------------------

AVATAR_MAX_SIZE = getattr(
    settings,
    "MEDIA_MAX_AVATAR_SIZE",
    2 * 1024 * 1024,
)

ALLOWED_ASPECT_RATIO = {
    (1, 1),
}

# -------------------------------------------------------
# Avatar Validation
# -------------------------------------------------------

def validate_avatar(
    *,
    file: UploadedFile,
) -> None:
    """
    Validate avatar image.
    """

    validate_image(
        file=file,
        max_size=AVATAR_MAX_SIZE,
    )

    image = validate_image_integrity(
        file=file,
    )

    validate_aspect_ratio(
        image=image,
        allowed=ALLOWED_ASPECT_RATIO,
    )