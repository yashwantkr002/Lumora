"""
===========================================================
File: app/services/profile/profile.py
===========================================================

PURPOSE

Business logic related to user profiles.

===========================================================
"""

import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from app.models.follow import UserFollow
from app.services.auth.activity import ActivityService

logger = logging.getLogger(__name__)

User = get_user_model()


class ProfileService:
    """
    Business logic for user profiles.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Get complete profile.
    #
    # -------------------------------------------------------

    @staticmethod
    def get_profile(username):

        return get_object_or_404(

            User.objects.select_related(
                "profile",
                "verification",
                "activity",
                "security",
            ),

            username=username,

        )

    # -------------------------------------------------------
    # FIX #2
    #
    # Update profile.
    #
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def update_profile(
        profile,
        cleaned_data,
        files,
    ):

        profile.bio = cleaned_data.get(
            "bio",
            profile.bio,
        )

        profile.website = cleaned_data.get(
            "website",
            profile.website,
        )

        profile.location = cleaned_data.get(
            "location",
            profile.location,
        )

        profile.profession = cleaned_data.get(
            "profession",
            profile.profession,
        )

        if files.get("avatar"):

            profile.avatar = files["avatar"]

        if files.get("cover_image"):

            profile.cover_image = files["cover_image"]

        profile.save(
            update_fields=[
                "bio",
                "website",
                "location",
                "profession",
                "avatar",
                "cover_image",
            ],
        )

        logger.info(
            "Profile updated.",
            extra={
                "user_id": profile.user.id,
            },
        )

        return profile

    # -------------------------------------------------------
    # FIX #3
    #
    # Followers.
    #
    # -------------------------------------------------------

    @staticmethod
    def get_followers(user):

        return (

            UserFollow.objects

            .filter(
                following=user,
            )

            .select_related(
                "follower",
                "follower__profile",
            )

            .order_by(
                "-created_at",
            )

        )

    # -------------------------------------------------------
    # FIX #4
    #
    # Following.
    #
    # -------------------------------------------------------

    @staticmethod
    def get_following(user):

        return (

            UserFollow.objects

            .filter(
                follower=user,
            )

            .select_related(
                "following",
                "following__profile",
            )

            .order_by(
                "-created_at",
            )

        )

    # -------------------------------------------------------
    # FIX #5
    #
    # Check follow status.
    #
    # Keeps follow logic out of Views.
    #
    # -------------------------------------------------------

    @staticmethod
    def is_following(
        current_user,
        profile_user,
    ):

        if current_user == profile_user:
            return False

        return UserFollow.objects.filter(
            follower=current_user,
            following=profile_user,
        ).exists()

    # -------------------------------------------------------
    # FIX #6
    #
    # Search users.
    #
    # -------------------------------------------------------

    @staticmethod
    def search_users(query):

        query = query.strip()

        if not query:

            return User.objects.none()

        return (

            User.objects

            .select_related(
                "profile",
            )

            .filter(

                Q(username__icontains=query)

                |

                Q(first_name__icontains=query)

                |

                Q(last_name__icontains=query)

                |

                Q(email__icontains=query)

            )

            .order_by(
                "username",
            )

        )

    # -------------------------------------------------------
    # FIX #7
    #
    # Soft deactivate account.
    #
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def deactivate_account(user):

        ActivityService.mark_offline(
            user,
        )

        user.is_active = False

        user.save(
            update_fields=[
                "is_active",
            ],
        )

        logger.warning(
            "User account deactivated.",
            extra={
                "user_id": user.id,
            },
        )

        return user