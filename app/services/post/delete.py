"""
===========================================================
File: app/services/post/delete.py
===========================================================

PURPOSE

Handles deletion of posts.

Supports:

• Permission Validation
• Soft Delete
• Logging

===========================================================
"""

import logging

from django.core.exceptions import PermissionDenied
from django.db import transaction

from app.models.post import Post
from app.services.media.upload_service import UploadService

logger = logging.getLogger(__name__)


class DeletePostService:
    """
    Handles deletion of posts.
    """

    # -------------------------------------------------------
    # Delete Post
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def delete_post(
        *,
        post: Post,
        user,
    ) -> None:
        """
        Soft delete a post.

        Only the owner can delete it.
        """

        # -------------------------------------------------------
        # Permission Check
        # -------------------------------------------------------

        if post.author != user:

            raise PermissionDenied(
                "You are not allowed to delete this post."
            )

        # -------------------------------------------------------
        # Delete attached media from storage
        # -------------------------------------------------------

        upload_service = UploadService()

        for media in post.media.all():
            if media.image:
                upload_service.delete(file_path=media.image.name)
            if media.video:
                upload_service.delete(file_path=media.video.name)

        # -------------------------------------------------------
        # Soft Delete
        # -------------------------------------------------------

        post.delete()

        # -------------------------------------------------------
        # Logging
        # -------------------------------------------------------

        logger.info(
            "Post deleted successfully.",
            extra={
                "post_id": post.id,
                "author_id": user.id,
            },
        )