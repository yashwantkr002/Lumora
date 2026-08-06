"""
===========================================================
File: app/core/storage/types.py
===========================================================

PURPOSE

Shared storage data models.

Returned by every storage provider.

Supported Providers

• Local Storage
• Cloudinary
• Amazon S3
• Azure Blob

===========================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class StoredFile:
    """
    Represents a stored media file.
    """

    provider: str

    path: str

    url: str

    filename: str

    content_type: str | None = None

    size: int | None = None

    width: int | None = None

    height: int | None = None

    public_id: str | None = None

    version: str | None = None

    format: str | None = None