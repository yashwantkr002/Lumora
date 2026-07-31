"""
===========================================================
File: app/services/save/query.py
===========================================================

PURPOSE

Provides optimized querysets for bookmarks.

Used by:

• SaveToggleService

===========================================================
"""

from django.db.models import QuerySet

from app.models.post import Post
from app.models.save import Save


class SaveQueryService:
    """
    Shared optimized querysets for bookmarks.
    """

    # -------------------------------------------------------
    # Base Queryset
    # -------------------------------------------------------

    @staticmethod
    def base_queryset() -> QuerySet[Save]:
        """
        Base queryset.
        """

        return (
            Save.objects
            .select_related(
                "user",
                "user__profile",
                "post",
                "post__author",
                "post__author__profile",
            )
        )

    # -------------------------------------------------------
    # User Bookmarks
    # -------------------------------------------------------

    @staticmethod
    def user_queryset(
        *,
        user,
    ) -> QuerySet[Save]:
        """
        Return bookmarks created by a user.
        """

        return (
            SaveQueryService
            .base_queryset()
            .filter(
                user=user,
            )
            .order_by(
                "-created_at",
            )
        )

    # -------------------------------------------------------
    # Saved Posts
    # -------------------------------------------------------

    @staticmethod
    def saved_posts(
        *,
        user,
    ) -> QuerySet[Post]:
        """
        Return bookmarked posts.
        """

        return (
            Post.objects
            .select_related(
                "author",
                "author__profile",
            )
            .prefetch_related(
                "tags",
            )
            .filter(
                saves__user=user,
            )
            .order_by(
                "-saves__created_at",
            )
        )

    # -------------------------------------------------------
    # User Bookmark
    # -------------------------------------------------------

    @staticmethod
    def get_user_save(
        *,
        user,
        post,
    ) -> Save | None:
        """
        Return user's bookmark for a post.
        """

        return (
            Save.objects
            .filter(
                user=user,
                post=post,
            )
            .first()
        )