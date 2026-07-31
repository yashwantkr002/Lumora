"""
===========================================================
File: app/services/post/reels.py
===========================================================

PURPOSE

Handles reels feed generation.

Supports:

• Public Reels
• Following Reels
• User Reels

===========================================================
"""

import logging

from django.db.models import Q, QuerySet

from app.models.follow import UserFollow
from app.models.post import Post
from app.models.post_media import PostMedia
from app.models.user import CustomUser

from app.services.post.query import PostQueryService

logger = logging.getLogger(__name__)


class ReelsPostService:
    """
    Handles reels feed generation.
    """

    # -------------------------------------------------------
    # Public Reels
    # -------------------------------------------------------

    @staticmethod
    def get_public_reels() -> QuerySet[Post]:
        """
        Return public reels.
        """

        reels = (
            PostQueryService
            .public_queryset()
            .filter(
                media__media_type=PostMedia.MediaType.VIDEO,
            )
            .distinct()
            .order_by(
                "-created_at",
            )
        )

        logger.info(
            "Public reels loaded.",
        )

        return reels

    # -------------------------------------------------------
    # Personalized Reels
    # -------------------------------------------------------

    @staticmethod
    def get_feed_reels(
        *,
        user: CustomUser,
    ) -> QuerySet[Post]:
        """
        Return reels for the authenticated user.
        """

        following_ids = UserFollow.objects.filter(
            follower=user,
        ).values_list(
            "following_id",
            flat=True,
        )

        reels = (
            PostQueryService
            .base_queryset()
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
            .filter(
                media__media_type=PostMedia.MediaType.VIDEO,
            )
            .distinct()
            .order_by(
                "-created_at",
            )
        )

        logger.info(
            "Reels feed loaded.",
            extra={
                "user_id": user.id,
            },
        )

        return reels

    # -------------------------------------------------------
    # User Reels
    # -------------------------------------------------------

    @staticmethod
    def get_user_reels(
        *,
        user: CustomUser,
    ) -> QuerySet[Post]:
        """
        Return reels uploaded by a user.
        """

        return (
            PostQueryService
            .user_queryset(
                user=user,
            )
            .filter(
                media__media_type=PostMedia.MediaType.VIDEO,
            )
            .distinct()
            .order_by(
                "-created_at",
            )
        )