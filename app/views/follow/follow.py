"""
===========================================================
File: app/views/follow/follow.py
===========================================================

PURPOSE

Follow another user.

Business logic belongs to FollowService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.follow.follow import FollowService
from app.services.profile.profile import ProfileService

logger = logging.getLogger(__name__)


@login_required
@require_POST
def follow_user(request, username):
    """
    Follow a user.
    """

    try:

        # -------------------------------------------------------
        # FIX #1
        #
        # Load target profile.
        #
        # -------------------------------------------------------

        user_to_follow = ProfileService.get_profile(
            username,
        )

        # -------------------------------------------------------
        # FIX #2
        #
        # Delegate follow logic to FollowService.
        #
        # -------------------------------------------------------

        FollowService.follow_user(
            follower=request.user,
            following=user_to_follow,
        )

        messages.success(
            request,
            f"You are now following {user_to_follow.username}.",
        )

    except PermissionDenied:

        messages.error(
            request,
            "Permission denied.",
        )

    except Exception:

        logger.exception(
            "Unexpected error while following user.",
            extra={
                "user_id": request.user.id,
                "target_username": username,
            },
        )

        messages.error(
            request,
            "Unable to follow user.",
        )

    return redirect(
        "profile",
        username=username,
    )



