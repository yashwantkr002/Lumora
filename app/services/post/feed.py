"""
===========================================================
File: app/services/post/feed.py
===========================================================

PURPOSE

Handles home feed generation.

Supports:

• Public Posts
• Followers-only Posts
• User's Own Posts

===========================================================
"""

import logging

from django.db.models import Prefetch, Q, QuerySet

from app.models.follow import UserFollow
from app.models.post import Post
from app.models.post_media import PostMedia
from app.models.user import CustomUser

logger = logging.getLogger(__name__)


class FeedPostService:
    """
    Handles feed generation.
    """

    # -------------------------------------------------------
    # Base Query
    # -------------------------------------------------------

    @staticmethod
    def _base_queryset() -> QuerySet[Post]:
        """
        Optimized queryset used by all feed methods.
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
    # Home Feed
    # -------------------------------------------------------

    @staticmethod
    def get_feed(
        *,
        user: CustomUser,
    ) -> QuerySet[Post]:
        """
        Return personalized home feed.
        """

        following_ids = UserFollow.objects.filter(
            follower=user,
        ).values_list(
            "following_id",
            flat=True,
        )

        posts = (
            FeedPostService
            ._base_queryset()
            .filter(

                Q(author=user)

                |

                Q(
                    author_id__in=following_ids,
                    visibility=Post.Visibility.FOLLOWERS,
                )

                |

                Q(
                    visibility=Post.Visibility.PUBLIC,
                )

            )
            .order_by(
                "-created_at",
            )
        )

        logger.info(
            "Feed loaded.",
            extra={
                "user_id": user.id,
            },
        )

        return posts

    # -------------------------------------------------------
    # User Feed
    # -------------------------------------------------------

    @staticmethod
    def get_user_feed(
        *,
        user: CustomUser,
    ) -> QuerySet[Post]:
        """
        Return posts created by the user.
        """

        return (
            FeedPostService
            ._base_queryset()
            .filter(
                author=user,
            )
            .order_by(
                "-created_at",
            )
        )

    # -------------------------------------------------------
    # Public Feed
    # -------------------------------------------------------

    @staticmethod
    def get_public_feed() -> QuerySet[Post]:
        """
        Return only public posts.
        """

        return (
            FeedPostService
            ._base_queryset()
            .filter(
                visibility=Post.Visibility.PUBLIC,
            )
            .order_by(
                "-created_at",
            )
        )