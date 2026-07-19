"""
===========================================================
File: app/services/post/query.py
===========================================================

PURPOSE

Provides optimized querysets for posts.

Shared by:

• FeedService
• DetailPostService
• SearchService
• ReelsService
• ProfilePostService

===========================================================
"""

from django.db.models import Prefetch, QuerySet

from app.models.post import Post
from app.models.post_media import PostMedia


class PostQueryService:
    """
    Shared optimized querysets for posts.
    """

    # -------------------------------------------------------
    # Base Query
    # -------------------------------------------------------

    @staticmethod
    def base_queryset() -> QuerySet[Post]:
        """
        Optimized queryset used across the project.
        """

        return (
            Post.objects
            .select_related(
                "author",
                "author__profile",
            )
            .prefetch_related(
                "tags",
                Prefetch(
                    "media",
                    queryset=PostMedia.objects.order_by(
                        "order",
                    ),
                ),
            )
        )

    # -------------------------------------------------------
    # Public Posts
    # -------------------------------------------------------

    @staticmethod
    def public_queryset() -> QuerySet[Post]:
        """
        Public posts only.
        """

        return (
            PostQueryService
            .base_queryset()
            .filter(
                visibility=Post.Visibility.PUBLIC,
            )
        )

    # -------------------------------------------------------
    # User Posts
    # -------------------------------------------------------

    @staticmethod
    def user_queryset(
        *,
        user,
    ) -> QuerySet[Post]:
        """
        Posts created by a user.
        """

        return (
            PostQueryService
            .base_queryset()
            .filter(
                author=user,
            )
        )

    # -------------------------------------------------------
    # Single Post
    # -------------------------------------------------------

    @staticmethod
    def detail_queryset() -> QuerySet[Post]:
        """
        Optimized queryset for post detail pages.
        """

        return (
            PostQueryService
            .base_queryset()
        )

    # -------------------------------------------------------
    # Search
    # -------------------------------------------------------

    @staticmethod
    def searchable_queryset() -> QuerySet[Post]:
        """
        Queryset used for searching posts.
        """

        return (
            PostQueryService
            .public_queryset()
        )