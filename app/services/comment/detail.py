"""
===========================================================
File: app/services/comment/detail.py
===========================================================

PURPOSE

Handles retrieval of comments.

===========================================================
"""

import logging

from django.shortcuts import get_object_or_404

from app.models.comment import Comment

from app.services.comment.query import (
    CommentQueryService,
)

logger = logging.getLogger(__name__)


class CommentDetailService:
    """
    Handles comment retrieval.
    """

    # -------------------------------------------------------
    # Get Comment
    # -------------------------------------------------------

    @staticmethod
    def get_comment(
        *,
        comment_id,
    ) -> Comment:
        """
        Return a single comment.
        """

        comment = get_object_or_404(
            CommentQueryService.detail_queryset(),
            pk=comment_id,
        )

        logger.info(
            "Comment retrieved.",
            extra={
                "comment_id": comment.id,
            },
        )

        return comment

    # -------------------------------------------------------
    # Get Replies
    # -------------------------------------------------------

    @staticmethod
    def get_replies(
        *,
        comment: Comment,
    ):
        """
        Return replies for a comment.
        """

        return CommentQueryService.replies_queryset(
            parent=comment,
        )

    # -------------------------------------------------------
    # Get Post Comments
    # -------------------------------------------------------

    @staticmethod
    def get_post_comments(
        *,
        post,
    ):
        """
        Return top-level comments for a post.
        """

        return CommentQueryService.top_level_queryset(
            post=post,
        )