"""
===========================================================
File: app/services/like/utils.py
===========================================================

PURPOSE

Shared utility methods for likes.

Used by:

• LikeToggleService

===========================================================
"""

from django.db.models import F

from app.models.post import Post


class LikeUtilsService:
    """
    Shared helper methods for likes.
    """

    # -------------------------------------------------------
    # Increment Likes
    # -------------------------------------------------------

    @staticmethod
    def increment_post_likes(
        *,
        post: Post,
    ) -> None:
        """
        Increase the post like counter.
        """

        Post.objects.filter(
            pk=post.pk,
        ).update(
            likes_count=F("likes_count") + 1,
        )

    # -------------------------------------------------------
    # Decrement Likes
    # -------------------------------------------------------

    @staticmethod
    def decrement_post_likes(
        *,
        post: Post,
    ) -> None:
        """
        Decrease the post like counter.
        """

        Post.objects.filter(
            pk=post.pk,
        ).update(
            likes_count=F("likes_count") - 1,
        )

    # -------------------------------------------------------
    # Toggle Result
    # -------------------------------------------------------

    @staticmethod
    def build_toggle_result(
        *,
        liked: bool,
        post: Post,
    ) -> dict:
        """
        Return the toggle response.
        """

        post.refresh_from_db(
            fields=[
                "likes_count",
            ],
        )

        return {
            "liked": liked,
            "likes_count": post.likes_count,
        }