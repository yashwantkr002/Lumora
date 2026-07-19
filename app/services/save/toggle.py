"""
===========================================================
File: app/services/save/toggle.py
===========================================================

PURPOSE

Handles bookmark toggling for posts.

===========================================================
"""

import logging

from django.db import transaction

from app.models.save import Save
from app.models.post import Post
from app.models.user import CustomUser

from app.services.save.query import (
    SaveQueryService,
)
from app.services.save.utils import (
    SaveUtilsService,
)

logger = logging.getLogger(__name__)


class SaveToggleService:
    """
    Handles bookmark toggle operations.
    """

    @staticmethod
    @transaction.atomic
    def toggle_save(
        *,
        post: Post,
        user: CustomUser,
    ) -> dict:
        """
        Toggle bookmark for a post.

        Returns:

        {
            "saved": bool,
            "saves_count": int,
        }
        """

        # -------------------------------------------------------
        # Existing Bookmark
        # -------------------------------------------------------

        save = SaveQueryService.get_user_save(
            user=user,
            post=post,
        )

        # -------------------------------------------------------
        # Remove Bookmark
        # -------------------------------------------------------

        if save:

            save.delete()

            SaveUtilsService.decrement_post_saves(
                post=post,
            )

            logger.info(
                "Post unsaved.",
                extra={
                    "post_id": post.id,
                    "user_id": user.id,
                },
            )

            return SaveUtilsService.build_toggle_result(
                saved=False,
                post=post,
            )

        # -------------------------------------------------------
        # Create Bookmark
        # -------------------------------------------------------

        Save.objects.create(
            user=user,
            post=post,
        )

        SaveUtilsService.increment_post_saves(
            post=post,
        )

        logger.info(
            "Post saved.",
            extra={
                "post_id": post.id,
                "user_id": user.id,
            },
        )

        return SaveUtilsService.build_toggle_result(
            saved=True,
            post=post,
        )