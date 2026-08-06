"""
===========================================================
File: app/core/storage/cloudinary.py
===========================================================

PURPOSE

Cloudinary storage backend.

Implements BaseStorage.

===========================================================
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

import cloudinary.uploader

from django.core.files.uploadedfile import UploadedFile

from .base import BaseStorage
from .types import StoredFile

logger = logging.getLogger(__name__)


class CloudinaryStorage(BaseStorage):
    """
    Cloudinary implementation.
    """

    def upload(
        self,
        *,
        file: UploadedFile,
        folder: str,
    ) -> StoredFile:

        resolved_folder = self.resolve_folder(folder)

        file_name = Path(file.name).stem or "upload"
        digest = hashlib.sha256(file.read()).hexdigest()[:16]
        public_id = f"{resolved_folder}/{file_name}-{digest}"

        file.seek(0)

        resource_type = "image"
        if file.content_type and file.content_type.startswith("video/"):
            resource_type = "video"

        result = cloudinary.uploader.upload(
            file,
            folder=resolved_folder,
            public_id=public_id,
            resource_type=resource_type,
            overwrite=True,
        )

        logger.info(
            "Uploaded to Cloudinary.",
            extra={
                "public_id": result["public_id"],
            },
        )

        return StoredFile(
            provider="cloudinary",
            path=result["public_id"],
            url=result["secure_url"],
            filename=file.name,
            content_type=result.get("resource_type"),
            size=result.get("bytes"),
            width=result.get("width"),
            height=result.get("height"),
            public_id=result["public_id"],
            version=str(result.get("version")),
            format=result.get("format"),
        )

    def delete(
        self,
        *,
        file_path: str,
    ) -> None:
        if not file_path:
            return

        public_id = file_path
        if public_id.startswith("http://") or public_id.startswith("https://"):
            public_id = public_id.split("/")[-1].split(".")[0]

        cloudinary.uploader.destroy(
            public_id,
            invalidate=True,
        )

    def exists(
        self,
        *,
        file_path: str,
    ) -> bool:

        return True

    def url(self, name: str, *args, **kwargs) -> str:
        if not name:
            return ""

        if name.startswith("http://") or name.startswith("https://"):
            return name

        cloud_name = cloudinary.config().cloud_name
        if not cloud_name:
            return name

        return cloudinary.CloudinaryResource(name).build_url()

    def metadata(
        self,
        *,
        file_path: str,
    ) -> StoredFile:

        return StoredFile(
            provider="cloudinary",
            path=file_path,
            url=self.url(file_path=file_path),
            filename=file_path.split("/")[-1],
            content_type=None,
            size=None,
            width=None,
            height=None,
            public_id=file_path,
            version=None,
            format=None,
        )