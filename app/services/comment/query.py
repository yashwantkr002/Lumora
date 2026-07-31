"""
===========================================================
File: app/services/comment/query.py
===========================================================

PURPOSE

Provides optimized querysets for comments.

Used by:

• CommentCreateService
• CommentUpdateService
• CommentDeleteService
• CommentDetailService

===========================================================
"""

from django.db.models import Prefetch, QuerySet

from app.models.comment import Comment


class CommentQueryService:
    """
    Shared optimized querysets for comments.
    """

    # -------------------------------------------------------
    # Base Queryset
    # -------------------------------------------------------

    @staticmethod
    def base_queryset() -> QuerySet[Comment]:
        """
        Optimized queryset used throughout the project.
        """

        return (
            Comment.objects
            .select_related(
                "author",
                "author__profile",
                "post",
                "parent",
            )
            .prefetch_related(
                Prefetch(
                    "replies",
                    queryset=Comment.objects.select_related(
                        "author",
                        "author__profile",
                    ).order_by(
                        "created_at",
                    ),
                ),
            )
        )

    # -------------------------------------------------------
    # Top-Level Comments
    # -------------------------------------------------------

    @staticmethod
    def top_level_queryset(
        *,
        post,
    ) -> QuerySet[Comment]:
        """
        Return top-level comments for a post.
        """

        return (
            CommentQueryService
            .base_queryset()
            .filter(
                post=post,
                parent__isnull=True,
                is_hidden=False,
            )
            .order_by(
                "-is_pinned",
                "created_at",
            )
        )

    # -------------------------------------------------------
    # Replies
    # -------------------------------------------------------

    @staticmethod
    def replies_queryset(
        *,
        parent,
    ) -> QuerySet[Comment]:
        """
        Return replies for a comment.
        """

        return (
            CommentQueryService
            .base_queryset()
            .filter(
                parent=parent,
                is_hidden=False,
            )
            .order_by(
                "created_at",
            )
        )

    # -------------------------------------------------------
    # User Comments
    # -------------------------------------------------------

    @staticmethod
    def user_queryset(
        *,
        user,
    ) -> QuerySet[Comment]:
        """
        Return comments created by a user.
        """

        return (
            CommentQueryService
            .base_queryset()
            .filter(
                author=user,
            )
            .order_by(
                "-created_at",
            )
        )

    # -------------------------------------------------------
    # Detail
    # -------------------------------------------------------

    @staticmethod
    def detail_queryset() -> QuerySet[Comment]:
        """
        Optimized queryset for comment detail.
        """

        return (
            CommentQueryService
            .base_queryset()
        )