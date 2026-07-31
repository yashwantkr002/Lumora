"""
===========================================================
File: app/services/post/profile.py
===========================================================

PURPOSE

Handles post retrieval for user profile pages.

Responsibilities

• Get posts of a specific user
• Optimize database queries
• Prepare queryset for pagination

===========================================================
"""

import logging

from app.models.post import Post

logger = logging.getLogger(__name__)


class ProfilePostService:
    """
    Handles profile post retrieval.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Get all posts created by a user.
    #
    # Returns a queryset so views can paginate.
    #
    # -------------------------------------------------------

    @staticmethod
    def get_user_posts(user):

        queryset = (

            Post.objects

            .filter(
                author=user,
            )

            .select_related(
                "author",
                "author__profile",
            )

            .prefetch_related(
                "likes",
                "comments",
            )

            .order_by(
                "-created_at",
            )

        )

        logger.info(
            "Profile posts loaded.",
            extra={
                "user_id": user.id,
            },
        )

        return queryset