"""
===========================================================
File: app/urls/profile.py
===========================================================

PURPOSE

Profile URL configuration.

Handles:

• Profile pages
• Profile editing
• Followers / Following
• Follow / Unfollow actions

===========================================================
"""

from django.urls import path

from app.views.profile.edit_profile import edit_profile
from app.views.profile.profile import profile

from app.views.follow.follow import follow_user
from app.views.follow.unfollow import unfollow_user
from app.views.follow.followers import followers
from app.views.follow.following import following

urlpatterns = [

    # -------------------------------------------------------
    # FIX #1
    #
    # Edit authenticated user's profile.
    #
    # -------------------------------------------------------

    path(
        "edit/",
        edit_profile,
        name="edit_profile",
    ),

    # -------------------------------------------------------
    # FIX #2
    #
    # Follow user.
    #
    # -------------------------------------------------------

    path(
        "<str:username>/follow/",
        follow_user,
        name="follow_user",
    ),

    # -------------------------------------------------------
    # FIX #3
    #
    # Unfollow user.
    #
    # -------------------------------------------------------

    path(
        "<str:username>/unfollow/",
        unfollow_user,
        name="unfollow_user",
    ),

    # -------------------------------------------------------
    # FIX #4
    #
    # Followers page.
    #
    # -------------------------------------------------------

    path(
        "<str:username>/followers/",
        followers,
        name="followers",
    ),

    # -------------------------------------------------------
    # FIX #5
    #
    # Following page.
    #
    # -------------------------------------------------------

    path(
        "<str:username>/following/",
        following,
        name="following",
    ),

    # -------------------------------------------------------
    # FIX #6
    #
    # Public profile.
    #
    # -------------------------------------------------------

    path(
        "<str:username>/",
        profile,
        name="profile",
    ),
]