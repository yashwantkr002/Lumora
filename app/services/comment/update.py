"""
===========================================================
File: app/services/comment/update.py
===========================================================

PURPOSE

Handles updating existing comments.

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


class CommentUpdateService:
    """
    Handles updating existing comments.
    """

    @staticmethod
    @transaction.atomic
    def update_comment(
        *,
        comment: Comment,
        user: CustomUser,
        content: str,
    ) -> Comment:
        """
        Update an existing comment.
        """

        # -------------------------------------------------------
        # Permission
        # -------------------------------------------------------

        CommentPermissionService.require_edit_permission(
            comment=comment,
            user=user,
        )

        # -------------------------------------------------------
        # Normalize Content
        # -------------------------------------------------------

        content = (
            CommentUtilsService
            .normalize_content(
                content=content,
            )
        )

        # -------------------------------------------------------
        # Validate Content
        # -------------------------------------------------------

        if not content:

            raise ValueError(
                "Comment cannot be empty."
            )

        # -------------------------------------------------------
        # Skip Unchanged Content
        # -------------------------------------------------------

        if comment.content == content:

            logger.info(
                "Comment update skipped (no changes).",
                extra={
                    "comment_id": comment.id,
                    "user_id": user.id,
                },
            )

            return comment

        # -------------------------------------------------------
        # Update Comment
        # -------------------------------------------------------

        comment.content = content

        CommentUtilsService.mark_as_edited(
            comment=comment,
        )

        comment.full_clean()

        comment.save(
            update_fields=[
                "content",
                "is_edited",
                "updated_at",
            ],
        )

        logger.info(
            "Comment updated.",
            extra={
                "comment_id": comment.id,
                "user_id": user.id,
            },
        )

        return comment