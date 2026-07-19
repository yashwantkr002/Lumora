"""
===========================================================
File: app/services/like/query.py
===========================================================

PURPOSE

Provides optimized querysets for likes.

Used by:

• LikeToggleService

===========================================================
"""

from django.db.models import QuerySet

from app.models.like import Like


class LikeQueryService:
    """
    Shared optimized querysets for likes.
    """

    # -------------------------------------------------------
    # Base Queryset
    # -------------------------------------------------------

    @staticmethod
    def base_queryset() -> QuerySet[Like]:
        """
        Base queryset.
        """

        return (
            Like.objects
            .select_related(
                "user",
                "user__profile",
                "post",
                "post__author",
            )
        )

    # -------------------------------------------------------
    # User Likes
    # -------------------------------------------------------

    @staticmethod
    def user_queryset(
        *,
        user,
    ) -> QuerySet[Like]:
        """
        Return likes created by a user.
        """

        return (
            LikeQueryService
            .base_queryset()
            .filter(
                user=user,
            )
            .order_by(
                "-created_at",
            )
        )

    # -------------------------------------------------------
    # Post Likes
    # -------------------------------------------------------

    @staticmethod
    def post_queryset(
        *,
        post,
    ) -> QuerySet[Like]:
        """
        Return likes for a post.
        """

        return (
            LikeQueryService
            .base_queryset()
            .filter(
                post=post,
            )
            .order_by(
                "-created_at",
            )
        )

    # -------------------------------------------------------
    # User Like
    # -------------------------------------------------------

    @staticmethod
    def user_like(
        *,
        user,
        post,
    ) -> QuerySet[Like]:
        """
        Return the user's like for a post.
        """

        return (
            LikeQueryService
            .base_queryset()
            .filter(
                user=user,
                post=post,
            )
        )