"""
===========================================================
File: app/services/post/update.py
===========================================================

PURPOSE

Handles updating existing posts.

Supports:

• Caption
• Location
• Visibility
• Post Settings
• Media Replacement
• Automatic Hashtag Parsing

===========================================================
"""

import logging
from typing import Iterable

from django.core.exceptions import PermissionDenied
from django.db import transaction

from app.models.post import Post
from app.models.post_media import PostMedia

from app.services.post.utils import PostUtils

logger = logging.getLogger(__name__)


class UpdatePostService:
    """
    Handles updating posts.
    """

    @staticmethod
    @transaction.atomic
    def update_post(
        *,
        post: Post,
        user,
        cleaned_data: dict,
        media_files: Iterable,
    ) -> Post:
        """
        Update an existing post.
        """

        # -------------------------------------------------------
        # Permission Check
        # -------------------------------------------------------

        if post.author != user:

            raise PermissionDenied(
                "You are not allowed to update this post."
            )

        # -------------------------------------------------------
        # Update Post Fields
        # -------------------------------------------------------

        post.caption = cleaned_data.get(
            "caption",
            post.caption,
        )

        post.location = cleaned_data.get(
            "location",
            post.location,
        )

        post.visibility = cleaned_data.get(
            "visibility",
            post.visibility,
        )

        post.allow_comments = cleaned_data.get(
            "allow_comments",
            post.allow_comments,
        )

        post.allow_download = cleaned_data.get(
            "allow_download",
            post.allow_download,
        )

        post.full_clean()

        post.save()

        # -------------------------------------------------------
        # Replace Media (Optional)
        # -------------------------------------------------------

        if media_files:

            post.media.all().delete()

            order = 1

            for file in media_files:

                PostUtils.create_media(
                    post=post,
                    file=file,
                    order=order,
                )

                order += 1

        # -------------------------------------------------------
        # Update Hashtags
        # -------------------------------------------------------

        hashtags = PostUtils.extract_hashtags(
            post.caption,
        )

        PostUtils.attach_tags(
            post=post,
            hashtags=hashtags,
        )

        logger.info(
            "Post updated successfully.",
            extra={
                "post_id": post.id,
                "user_id": user.id,
                "media_count": post.media.count(),
            },
        )

        return post