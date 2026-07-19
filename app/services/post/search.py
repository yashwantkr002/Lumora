"""
===========================================================
File: app/services/post/search.py
===========================================================

PURPOSE

Handles searching posts.

Supports:

• Caption Search
• Hashtag Search
• Author Search
• Public Posts Only

===========================================================
"""

import logging

from django.db.models import Q, QuerySet

from app.models.post import Post
from app.services.post.query import PostQueryService

logger = logging.getLogger(__name__)


class SearchPostService:
    """
    Handles post searching.
    """

    # -------------------------------------------------------
    # Search Posts
    # -------------------------------------------------------

    @staticmethod
    def search_posts(
        *,
        query: str,
    ) -> QuerySet[Post]:
        """
        Search public posts by caption,
        hashtag, or author's username.
        """

        query = query.strip()

        if not query:

            return Post.objects.none()

        posts = (
            PostQueryService
            .searchable_queryset()
            .filter(
                Q(caption__icontains=query)
                |
                Q(tags__name__icontains=query)
                |
                Q(author__username__icontains=query)
            )
            .distinct()
            .order_by(
                "-created_at",
            )
        )

        logger.info(
            "Post search completed.",
            extra={
                "query": query,
                "results": posts.count(),
            },
        )

        return posts

    # -------------------------------------------------------
    # Hashtag Search
    # -------------------------------------------------------

    @staticmethod
    def search_hashtag(
        *,
        hashtag: str,
    ) -> QuerySet[Post]:
        """
        Return posts matching a hashtag.
        """

        hashtag = hashtag.strip().lstrip("#").lower()

        return (
            PostQueryService
            .searchable_queryset()
            .filter(
                tags__slug=hashtag,
            )
            .order_by(
                "-created_at",
            )
        )

    # -------------------------------------------------------
    # Author Search
    # -------------------------------------------------------

    @staticmethod
    def search_author(
        *,
        username: str,
    ) -> QuerySet[Post]:
        """
        Return posts by username.
        """

        return (
            PostQueryService
            .searchable_queryset()
            .filter(
                author__username__iexact=username,
            )
            .order_by(
                "-created_at",
            )
        )