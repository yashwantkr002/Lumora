"""
===========================================================
File: app/models/tag.py
===========================================================

PURPOSE

Stores hashtags used by posts.

Each tag is unique and can be attached
to multiple posts.

===========================================================
"""

from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)


class Tag(
    UUIDModel,
    TimeStampedModel,
):
    """
    Hashtag model.
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique hashtag name.",
    )

    slug = models.SlugField(
        unique=True,
        db_index=True,
        help_text="URL-friendly hashtag.",
    )

    class Meta:

        db_table = "tags"

        ordering = (
            "name",
        )

        indexes = [

            models.Index(
                fields=[
                    "name",
                ]
            ),

            models.Index(
                fields=[
                    "slug",
                ]
            ),

        ]

    def __str__(self) -> str:

        return self.name