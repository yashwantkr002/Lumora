"""
===========================================================
File: app/services/comment/delete.py
===========================================================

PURPOSE

Handles deleting comments.

===========================================================
"""

import logging

from django.db import transaction

from app.models.comment import Comment
from app.models.user import CustomUser

from app.services.comment.permissions import (
    CommentPermissionService,
)
from app.services.comment.utils import (
    CommentUtilsService,
)

logger = logging.getLogger(__name__)


class CommentDeleteService:
    """
    Handles deleting comments.
    """

    @staticmethod
    @transaction.atomic
    def delete_comment(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> None:
        """
        Soft delete a comment.
        """

        # -------------------------------------------------------
        # Permission
        # -------------------------------------------------------

        CommentPermissionService.require_delete_permission(
            comment=comment,
            user=user,
        )

        # -------------------------------------------------------
        # Prevent Double Delete
        # -------------------------------------------------------

        if comment.is_deleted:

            logger.info(
                "Comment already deleted.",
                extra={
                    "comment_id": comment.id,
                    "user_id": user.id,
                },
            )

            return

        # -------------------------------------------------------
        # Update Analytics
        # -------------------------------------------------------

        CommentUtilsService.decrement_post_comments(
            post=comment.post,
        )

        CommentUtilsService.decrement_reply_count(
            parent=comment.parent,
        )

        # -------------------------------------------------------
        # Soft Delete
        # -------------------------------------------------------

        comment.soft_delete()

        logger.info(
            "Comment deleted.",
            extra={
                "comment_id": comment.id,
                "post_id": comment.post.id,
                "user_id": user.id,
            },
        )