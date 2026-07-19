"""
===========================================================
File: app/views/profile/following.py
===========================================================

PURPOSE

Display the users followed by a profile.

Business logic belongs to ProfileService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.services.profile.profile import ProfileService

logger = logging.getLogger(__name__)


@login_required
def following(request, username):
    """
    Display users followed by a specific user.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Load profile through ProfileService.
    #
    # -------------------------------------------------------

    profile_user = ProfileService.get_profile(
        username,
    )

    # -------------------------------------------------------
    # FIX #2
    #
    # Load following list through ProfileService.
    #
    # -------------------------------------------------------

    following = ProfileService.get_following(
        profile_user,
    )

    context = {
        "profile_user": profile_user,
        "following": following,
        "following_count": following.count(),
    }

    logger.info(
        "Following list viewed.",
        extra={
            "viewer_id": request.user.id,
            "profile_id": profile_user.id,
        },
    )

    return render(
        request,
        "profile/following.html",
        context,
    )