"""
===========================================================
File: app/services/media/image_service.py
===========================================================

PURPOSE

Image processing service.

Responsibilities

• Optimize images
• Resize images
• Compress images
• Convert images to WebP
• Generate thumbnails
• Extract metadata

Uploading is handled by UploadService.

===========================================================
"""

from __future__ import annotations

import logging
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

from PIL import Image

logger = logging.getLogger(__name__)


class ImageService:
    """
    Image processing service.
    """

    # -----------------------------------------------------
    # Optimize
    # -----------------------------------------------------

    def optimize(
        self,
        *,
        file: UploadedFile,
        quality: int = 85,
    ) -> ContentFile:
        """
        Optimize image.
        """

        image = Image.open(file)

        output = BytesIO()

        image.save(

            output,

            format=image.format,

            optimize=True,

            quality=quality,

        )

        output.seek(0)

        logger.info(

            "Image optimized.",

            extra={

                "filename": file.name,

            },

        )

        return ContentFile(

            output.read(),

            name=file.name,

        )

    # -----------------------------------------------------
    # Resize
    # -----------------------------------------------------

    def resize(
        self,
        *,
        file: UploadedFile,
        width: int,
        height: int,
    ) -> ContentFile:
        """
        Resize image.
        """

        image = Image.open(file)

        resized = image.resize(

            (

                width,

                height,

            )

        )

        output = BytesIO()

        resized.save(

            output,

            format=image.format,

        )

        output.seek(0)

        return ContentFile(

            output.read(),

            name=file.name,

        )

    # -----------------------------------------------------
    # Convert to WebP
    # -----------------------------------------------------

    def convert_to_webp(
        self,
        *,
        file: UploadedFile,
        quality: int = 85,
    ) -> ContentFile:
        """
        Convert image to WebP.
        """

        image = Image.open(file)

        output = BytesIO()

        image.save(

            output,

            format="WEBP",

            quality=quality,

            optimize=True,

        )

        output.seek(0)

        filename = file.name.rsplit(".", 1)[0]

        return ContentFile(

            output.read(),

            name=f"{filename}.webp",

        )

    # -----------------------------------------------------
    # Thumbnail
    # -----------------------------------------------------

    def create_thumbnail(
        self,
        *,
        file: UploadedFile,
        size: tuple[int, int] = (300, 300),
    ) -> ContentFile:
        """
        Create thumbnail.
        """

        image = Image.open(file)

        image.thumbnail(size)

        output = BytesIO()

        image.save(

            output,

            format=image.format,

        )

        output.seek(0)

        return ContentFile(

            output.read(),

            name=file.name,

        )

    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    def metadata(
        self,
        *,
        file: UploadedFile,
    ) -> dict:
        """
        Return image metadata.
        """

        image = Image.open(file)

        width, height = image.size

        return {

            "width": width,

            "height": height,

            "mode": image.mode,

            "format": image.format,

        }