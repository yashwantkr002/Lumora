"""
===========================================================
File: app/services/post/create.py
===========================================================

PURPOSE

Handles post creation.

Features

• Multiple Images
• Multiple Videos
• Mixed Media
• Automatic Hashtag Parsing
• Automatic Tag Creation

===========================================================
"""

import logging
import re
from typing import Iterable

from django.db import transaction
from django.utils.text import slugify

from app.models.post import Post
from app.models.post_media import PostMedia
from app.models.tag import Tag
from app.models.user import CustomUser

logger = logging.getLogger(__name__)


class CreatePostService:
    """
    Handles creation of posts.
    """

    HASHTAG_PATTERN = r"#([A-Za-z0-9_]+)"

    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def create_post(
        *,
        author: CustomUser,
        cleaned_data: dict,
        files,
    ) -> Post:
        """
        Create a post with media and hashtags.
        """

        post = CreatePostService._create_post(
            author=author,
            cleaned_data=cleaned_data,
        )

        CreatePostService._save_media(
            post=post,
            media_files=files.getlist("media"),
        )

        CreatePostService._attach_tags(
            post=post,
            caption=post.caption,
        )

        logger.info(
            "Post created successfully.",
            extra={
                "post_id": post.id,
                "author_id": author.id,
                "media_count": post.media.count(),
                "tag_count": post.tags.count(),
            },
        )

        return post

    # -------------------------------------------------------
    # Create Post
    # -------------------------------------------------------

    @staticmethod
    def _create_post(
        *,
        author: CustomUser,
        cleaned_data: dict,
    ) -> Post:

        return Post.objects.create(
            author=author,
            caption=cleaned_data.get(
                "caption",
                "",
            ),
            location=cleaned_data.get(
                "location",
                "",
            ),
            visibility=cleaned_data.get(
                "visibility",
                Post.Visibility.PUBLIC,
            ),
            allow_comments=cleaned_data.get(
                "allow_comments",
                True,
            ),
            allow_download=cleaned_data.get(
                "allow_download",
                False,
            ),
        )

    # -------------------------------------------------------
    # Save Media
    # -------------------------------------------------------

    @staticmethod
    def _save_media(
        *,
        post: Post,
        media_files,
    ) -> None:

        order = 1

        for file in media_files:

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

                continue

            media.full_clean()

            media.save()

            order += 1

    # -------------------------------------------------------
    # Attach Tags
    # -------------------------------------------------------

    @staticmethod
    def _attach_tags(
        *,
        post: Post,
        caption: str,
    ) -> None:

        hashtags = CreatePostService._extract_hashtags(
            caption,
        )

        if not hashtags:
            return

        tags = []

        for name in hashtags:

            tag, _ = Tag.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    "name": name,
                },
            )

            tags.append(tag)

        post.tags.set(tags)

    # -------------------------------------------------------
    # Extract Hashtags
    # -------------------------------------------------------

    @staticmethod
    def _extract_hashtags(
        caption: str,
    ) -> list[str]:
        """
        Extract unique hashtags from caption.
        """

        hashtags = re.findall(
            CreatePostService.HASHTAG_PATTERN,
            caption,
        )

        cleaned = []

        for tag in hashtags:

            normalized = tag.strip().lower()

            if normalized and normalized not in cleaned:

                cleaned.append(normalized)

        return cleaned