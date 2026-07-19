"""
===========================================================
File: app/services/post/detail.py
===========================================================

PURPOSE

Handles retrieval of a single post.

===========================================================
"""

import logging

from django.db.models import F
from django.shortcuts import get_object_or_404

from app.models.post import Post
from app.services.post.query import PostQueryService

logger = logging.getLogger(__name__)


class PostDetailService:
    """
    Handles post detail operations.
    """

    # -------------------------------------------------------
    # Get Post
    # -------------------------------------------------------

    @staticmethod
    def get_post(
        *,
        post_id,
    ) -> Post:
        """
        Return a post without modifying analytics.
        """

        return get_object_or_404(
            PostQueryService.detail_queryset(),
            pk=post_id,
        )

    # -------------------------------------------------------
    # Increment Views
    # -------------------------------------------------------

    @staticmethod
    def increment_views(
        *,
        post: Post,
    ) -> None:
        """
        Increment the post view counter.
        """

        Post.objects.filter(
            pk=post.pk,
        ).update(
            views_count=F("views_count") + 1,
        )

        post.refresh_from_db(
            fields=[
                "views_count",
            ]
        )

        logger.info(
            "Post view recorded.",
            extra={
                "post_id": post.id,
                "author_id": post.author.id,
            },
        )