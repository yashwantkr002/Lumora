"""
===========================================================
File: app/services/media/validators/common.py
===========================================================

PURPOSE

Common media validation utilities.

Reusable by:

• Image Validator
• Video Validator
• Avatar Validator
• Cover Validator
• Post Media Validator

===========================================================
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from app.services.media.exceptions import (
    InvalidFileExtension,
    InvalidFilename,
    InvalidMimeType,
    InvalidUploadFolder,
    MaxFileSizeExceeded,
)

# -------------------------------------------------------
# File Size
# -------------------------------------------------------

def validate_file_size(
    *,
    file: UploadedFile,
    max_size: int,
) -> None:
    """
    Validate uploaded file size.
    """

    if file.size > max_size:

        raise MaxFileSizeExceeded(
            f"Maximum allowed size is {max_size} bytes."
        )


# -------------------------------------------------------
# Extension
# -------------------------------------------------------

def validate_extension(
    *,
    file: UploadedFile,
    allowed_extensions: set[str],
) -> None:
    """
    Validate file extension.
    """

    extension = Path(file.name).suffix.lower()

    if extension not in allowed_extensions:

        raise InvalidFileExtension(extension)


# -------------------------------------------------------
# MIME Type
# -------------------------------------------------------

def validate_mime_type(
    *,
    file: UploadedFile,
    allowed_types: set[str],
) -> None:
    """
    Validate MIME type.
    """

    content_type = (
        getattr(file, "content_type", "")
        or ""
    ).lower()

    if content_type not in allowed_types:

        raise InvalidMimeType(content_type)


# -------------------------------------------------------
# Filename
# -------------------------------------------------------

FILENAME_PATTERN = re.compile(
    r"^[a-zA-Z0-9._-]+$"
)


def validate_filename(
    *,
    filename: str,
) -> None:
    """
    Validate original filename.
    """

    if not filename:

        raise InvalidFilename(
            "Filename cannot be empty."
        )

    if not FILENAME_PATTERN.match(filename):

        raise InvalidFilename(filename)


# -------------------------------------------------------
# Upload Folder
# -------------------------------------------------------

def validate_folder(
    *,
    folder: str,
) -> None:
    """
    Validate upload folder.
    """

    if folder not in settings.MEDIA_UPLOAD_FOLDERS:

        raise InvalidUploadFolder(folder)


# -------------------------------------------------------
# Sanitize Filename
# -------------------------------------------------------

def sanitize_filename(
    *,
    filename: str,
) -> str:
    """
    Convert filename into a safe format.
    """

    path = Path(filename)

    safe_name = re.sub(
        r"[^a-zA-Z0-9_-]",
        "-",
        path.stem,
    ).strip("-")

    extension = path.suffix.lower()

    return f"{safe_name}{extension}"


# -------------------------------------------------------
# Unique Filename
# -------------------------------------------------------

def generate_unique_filename(
    *,
    filename: str,
) -> str:
    """
    Generate collision-free filename.
    """

    sanitized = sanitize_filename(
        filename=filename,
    )

    path = Path(sanitized)

    return (
        f"{path.stem}-"
        f"{uuid.uuid4().hex}"
        f"{path.suffix}"
    )