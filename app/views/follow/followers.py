"""
===========================================================
File: app/views/follow/followers.py
===========================================================

PURPOSE

Display the followers of a user's profile.

Business logic belongs to ProfileService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.services.profile.profile import ProfileService

logger = logging.getLogger(__name__)


@login_required
def followers(request, username):
    """
    Display the followers of a user's profile.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Retrieve the requested user's profile through
    # ProfileService instead of querying the model directly.
    #
    # -------------------------------------------------------

    profile_user = ProfileService.get_profile(
        username=username,
    )

    # -------------------------------------------------------
    # FIX #2
    #
    # Retrieve followers through the service layer.
    #
    # -------------------------------------------------------

    followers = ProfileService.get_followers(
        profile_user,
    )

    # -------------------------------------------------------
    # FIX #3
    #
    # Prepare template context.
    #
    # -------------------------------------------------------

    context = {
        "profile_user": profile_user,
        "followers": followers,
        "followers_count": followers.count(),
    }

    # -------------------------------------------------------
    # FIX #4
    #
    # Structured logging.
    #
    # -------------------------------------------------------

    logger.info(
        "Followers page viewed.",
        extra={
            "viewer_id": request.user.id,
            "profile_id": profile_user.id,
        },
    )

    return render(
        request,
        "profile/followers.html",
        context,
    )