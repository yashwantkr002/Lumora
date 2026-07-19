"""
===========================================================
File: app/views/follow/unfollow.py
===========================================================

PURPOSE

Unfollow a user.

Business logic belongs to UnfollowService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.follow.unfollow import UnfollowService
from app.services.profile.profile import ProfileService

logger = logging.getLogger(__name__)


@login_required
@require_POST
def unfollow_user(request, username):
    """
    Unfollow a user.
    """

    try:

        user_to_unfollow = ProfileService.get_profile(
            username,
        )

        unfollowed = UnfollowService.unfollow_user(
            follower=request.user,
            following=user_to_unfollow,
        )

        if unfollowed:

            messages.success(
                request,
                f"You unfollowed {user_to_unfollow.username}.",
            )

        else:

            messages.info(
                request,
                f"You are not following {user_to_unfollow.username}.",
            )

    except Exception:

        logger.exception(
            "Unexpected error while unfollowing user.",
            extra={
                "user_id": request.user.id,
                "target_username": username,
            },
        )

        messages.error(
            request,
            "Unable to unfollow user.",
        )

    return redirect(
        "profile",
        username=username,
    )