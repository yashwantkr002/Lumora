"""
===========================================================
File: app/services/save/utils.py
===========================================================

PURPOSE

Shared utility methods for bookmarks.

Used by:

• SaveToggleService

===========================================================
"""

from django.db.models import F

from app.models.post import Post


class SaveUtilsService:
    """
    Shared helper methods for bookmarks.
    """

    # -------------------------------------------------------
    # Increment Saves
    # -------------------------------------------------------

    @staticmethod
    def increment_post_saves(
        *,
        post: Post,
    ) -> None:
        """
        Increase the post save counter.
        """

        Post.objects.filter(
            pk=post.pk,
        ).update(
            saves_count=F("saves_count") + 1,
        )

    # -------------------------------------------------------
    # Decrement Saves
    # -------------------------------------------------------

    @staticmethod
    def decrement_post_saves(
        *,
        post: Post,
    ) -> None:
        """
        Decrease the post save counter.
        """

        Post.objects.filter(
            pk=post.pk,
        ).update(
            saves_count=F("saves_count") - 1,
        )

    # -------------------------------------------------------
    # Toggle Response
    # -------------------------------------------------------

    @staticmethod
    def build_toggle_result(
        *,
        saved: bool,
        post: Post,
    ) -> dict:
        """
        Build bookmark toggle response.
        """

        post.refresh_from_db(
            fields=[
                "saves_count",
            ],
        )

        return {
            "saved": saved,
            "saves_count": post.saves_count,
        }