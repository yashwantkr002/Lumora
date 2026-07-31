"""
===========================================================
File: app/services/like/toggle.py
===========================================================

PURPOSE

Handles toggling likes for posts.

===========================================================
"""

import logging

from django.db import transaction

from app.models.like import Like
from app.models.post import Post
from app.models.user import CustomUser

from app.services.like.query import (
    LikeQueryService,
)
from app.services.like.utils import (
    LikeUtilsService,
)
from app.services.notification.create import (
    NotificationCreateService,
)

logger = logging.getLogger(__name__)


class LikeToggleService:
    """
    Handles like toggle operations.
    """

    @staticmethod
    @transaction.atomic
    def toggle_like(
        *,
        post: Post,
        user: CustomUser,
    ) -> dict:
        """
        Toggle a like for a post.

        Returns:
            {
                "liked": bool,
                "likes_count": int,
            }
        """

        # -------------------------------------------------------
        # Existing Like
        # -------------------------------------------------------

        like = (
            LikeQueryService
            .user_like(
                user=user,
                post=post,
            )
            .first()
        )

        # -------------------------------------------------------
        # Unlike
        # -------------------------------------------------------

        if like:

            like.delete()

            LikeUtilsService.decrement_post_likes(
                post=post,
            )

            logger.info(
                "Post unliked.",
                extra={
                    "post_id": post.id,
                    "user_id": user.id,
                },
            )

            return LikeUtilsService.build_toggle_result(
                liked=False,
                post=post,
            )

        # -------------------------------------------------------
        # Like
        # -------------------------------------------------------

        Like.objects.create(
            user=user,
            post=post,
        )

        LikeUtilsService.increment_post_likes(
            post=post,
        )

        logger.info(
            "Post liked.",
            extra={
                "post_id": post.id,
                "user_id": user.id,
            },
        )
        NotificationCreateService.create_notification(
            actor=user,
            recipient=post.author,
            post=post,
        )
        return LikeUtilsService.build_toggle_result(
            liked=True,
            post=post,
        )