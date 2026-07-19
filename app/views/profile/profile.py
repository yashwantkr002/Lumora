"""
===========================================================
File: app/views/profile/profile.py
===========================================================

PURPOSE

Display a user's public profile.

Business logic belongs to ProfileService
and ProfilePostService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.services.post.profile import ProfilePostService
from app.services.profile.profile import ProfileService

logger = logging.getLogger(__name__)


@login_required
def profile(request, username):
    """
    Display a user's public profile.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Get profile.
    #
    # -------------------------------------------------------

    profile_user = ProfileService.get_profile(
        username,
    )

    # -------------------------------------------------------
    # FIX #2
    #
    # Get user's posts.
    #
    # -------------------------------------------------------

    posts = ProfilePostService.get_user_posts(
        profile_user,
    )

    # -------------------------------------------------------
    # FIX #3
    #
    # Follow status handled by service.
    #
    # -------------------------------------------------------

    is_following = ProfileService.is_following(
        request.user,
        profile_user,
    )

    # -------------------------------------------------------
    # FIX #4
    #
    # Build template context.
    #
    # -------------------------------------------------------

    context = {
        "profile_user": profile_user,
        "posts": posts,
        "posts_count": posts.count(),
        "followers_count": ProfileService.get_followers(
            profile_user,
        ).count(),
        "following_count": ProfileService.get_following(
            profile_user,
        ).count(),
        "is_following": is_following,
    }

    logger.info(
        "Profile viewed.",
        extra={
            "viewer_id": request.user.id,
            "profile_id": profile_user.id,
        },
    )

    return render(
        request,
        "profile/profile.html",
        context,
    )