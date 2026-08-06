"""
===========================================================
File: app/services/media/validators/image.py
===========================================================

PURPOSE

Production-grade image validation.

Supports

• JPEG
• PNG
• WEBP
• GIF

===========================================================
"""

from __future__ import annotations

from typing import Final

from PIL import Image
from PIL import UnidentifiedImageError

from django.core.files.uploadedfile import UploadedFile

from app.services.media.exceptions import (
    InvalidAspectRatio,
    InvalidColorMode,
    InvalidImageDimensions,
    InvalidImageFile,
)

from .common import (
    validate_extension,
    validate_file_size,
    validate_mime_type,
)

# -------------------------------------------------------
# Constants
# -------------------------------------------------------

MIN_WIDTH: Final = 300
MIN_HEIGHT: Final = 300

ALLOWED_COLOR_MODES: Final = {
    "RGB",
    "RGBA",
}

SUPPORTED_EXTENSIONS: Final = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
}

SUPPORTED_MIME_TYPES: Final = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}
def validate_image(
    *,
    file: UploadedFile,
    max_size: int,
) -> None:
    """
    Full image validation.
    """

    validate_file_size(
        file=file,
        max_size=max_size,
    )

    validate_extension(
        file=file,
        allowed_extensions=SUPPORTED_EXTENSIONS,
    )

    validate_mime_type(
        file=file,
        allowed_types=SUPPORTED_MIME_TYPES,
    )

    image = validate_image_integrity(
        file=file,
    )

    validate_image_dimensions(
        image=image,
    )

    validate_color_mode(
        image=image,
    )

def validate_image_integrity(
    *,
    file: UploadedFile,
) -> Image.Image:
    """
    Verify uploaded image.
    """

    try:

        image = Image.open(file)

        image.verify()

        file.seek(0)

        return Image.open(file)

    except (
        UnidentifiedImageError,
        OSError,
    ) as exc:

        raise InvalidImageFile() from exc

def validate_image_dimensions(
    *,
    image: Image.Image,
) -> None:

    width, height = image.size

    if width < MIN_WIDTH:

        raise InvalidImageDimensions()

    if height < MIN_HEIGHT:

        raise InvalidImageDimensions()

def validate_aspect_ratio(
    *,
    image: Image.Image,
    allowed: set[tuple[int, int]],
) -> None:

    width, height = image.size

    ratio = round(width / height, 2)

    allowed_ratios = {
        round(w / h, 2)
        for w, h in allowed
    }

    if ratio not in allowed_ratios:

        raise InvalidAspectRatio()

# -------------------------------------------------------
# Color Mode
# -------------------------------------------------------

def validate_color_mode(
    *,
    image: Image.Image,
) -> None:
    """
    Validate image color mode.
    """

    if image.mode not in ALLOWED_COLOR_MODES:

        raise InvalidColorMode(
            image.mode,
        )

# -------------------------------------------------------
# Metadata
# -------------------------------------------------------

def get_image_metadata(
    *,
    image: Image.Image,
) -> dict[str, str | int]:
    """
    Return image metadata.
    """

    width, height = image.size

    return {

        "width": width,

        "height": height,

        "mode": image.mode,

        "format": image.format,

    }


