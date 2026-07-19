"""
===========================================================
File: app/services/post/utils.py
===========================================================

PURPOSE

Reusable utilities for Post services.

Shared by:

• CreatePostService
• UpdatePostService
• FeedService
• ReelsService
• Future StoryService

===========================================================
"""

import re

from django.utils.text import slugify

from app.models.post import Post
from app.models.post_media import PostMedia
from app.models.tag import Tag


class PostUtils:
    """
    Shared helper methods for post services.
    """

    HASHTAG_PATTERN = r"#([A-Za-z0-9_]+)"

    # -------------------------------------------------------
    # Hashtags
    # -------------------------------------------------------

    @staticmethod
    def extract_hashtags(
        caption: str,
    ) -> list[str]:
        """
        Extract unique hashtags from caption.
        """

        hashtags = re.findall(
            PostUtils.HASHTAG_PATTERN,
            caption or "",
        )

        cleaned = []

        for tag in hashtags:

            tag = tag.strip().lower()

            if tag and tag not in cleaned:

                cleaned.append(tag)

        return cleaned

    # -------------------------------------------------------
    # Tags
    # -------------------------------------------------------

    @staticmethod
    def attach_tags(
        *,
        post: Post,
        hashtags: list[str],
    ) -> None:
        """
        Attach hashtags to a post.
        Missing tags are created automatically.
        """

        tags = []

        for hashtag in hashtags:

            tag, _ = Tag.objects.get_or_create(
                slug=slugify(hashtag),
                defaults={
                    "name": hashtag,
                },
            )

            tags.append(tag)

        post.tags.set(tags)

    # -------------------------------------------------------
    # Media
    # -------------------------------------------------------

    @staticmethod
    def create_media(
        *,
        post: Post,
        file,
        order: int,
    ) -> PostMedia:
        """
        Create a PostMedia object.
        """

        content_type = file.content_type or ""

        media = PostMedia(
            post=post,
            order=order,
        )

        if content_type.startswith("image/"):

            media.media_type = (
                PostMedia.MediaType.IMAGE
            )

            media.image = file

        elif content_type.startswith("video/"):

            media.media_type = (
                PostMedia.MediaType.VIDEO
            )

            media.video = file

        else:

            raise ValueError(
                f"Unsupported media type: {content_type}"
            )

        media.full_clean()

        media.save()

        return media

    # -------------------------------------------------------
    # Replace Media
    # -------------------------------------------------------

    @staticmethod
    def replace_media(
        *,
        post: Post,
        media_files,
    ) -> None:
        """
        Replace all media attached to a post.
        """

        post.media.all().delete()

        order = 1

        for file in media_files:

            PostUtils.create_media(
                post=post,
                file=file,
                order=order,
            )

            order += 1