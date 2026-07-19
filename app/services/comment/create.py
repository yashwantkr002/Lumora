"""
===========================================================
File: app/services/comment/create.py
===========================================================

PURPOSE

Handles comment creation.

===========================================================
"""

import logging

from django.db import transaction

from app.models.comment import Comment
from app.models.notification import Notification
from app.models.post import Post

from app.services.comment.utils import (
    CommentUtilsService,
)
from app.services.notification.create import NotificationCreateService

logger = logging.getLogger(__name__)


class CommentCreateService:
    """
    Handles comment creation.
    """

    @staticmethod
    @transaction.atomic
    def create_comment(
        *,
        post: Post,
        author,
        content: str,
        parent: Comment | None = None,
    ) -> Comment:
        """
        Create a comment or reply.
        """

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
        # Validate Parent
        # -------------------------------------------------------

        CommentUtilsService.validate_parent(
            post=post,
            parent=parent,
        )

        # -------------------------------------------------------
        # Create Comment
        # -------------------------------------------------------

        comment = Comment.objects.create(
            post=post,
            author=author,
            parent=parent,
            content=content,
        )
        if parent:
            NotificationCreateService.create_notification(
                actor=author,
                recipient=parent.author,
                notification_type=Notification.NotificationType.REPLY,
                post=post,
                comment=comment,
            )
        else:
            NotificationCreateService.create_notification(
                actor=author,
                recipient=post.author,
                notification_type=Notification.NotificationType.COMMENT,
                post=post,
                comment=comment,
            )
        # -------------------------------------------------------
        # Update Analytics
        # -------------------------------------------------------

        CommentUtilsService.increment_post_comments(
            post=post,
        )

        CommentUtilsService.increment_reply_count(
            parent=parent,
        )

        logger.info(
            "Comment created.",
            extra={
                "comment_id": comment.id,
                "post_id": post.id,
                "author_id": author.id,
                "parent_id": (
                    parent.id
                    if parent
                    else None
                ),
            },
        )

        return comment