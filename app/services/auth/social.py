import logging

from django.db import transaction

from app.models.user import (
    UserProfile,
    UserVerification,
    UserActivity,
    UserSecurity,
)

logger = logging.getLogger(__name__)


class SocialAuthService:
    """
    Handles application-specific tasks after
    successful social authentication.
    """

    @staticmethod
    @transaction.atomic
    def initialize_social_user(user):
        """
        Create all related records
        for first-time social login.
        """

        UserProfile.objects.get_or_create(
            user=user,
        )

        UserVerification.objects.get_or_create(
            user=user,
            defaults={
                "is_verified": True,
            },
        )

        UserActivity.objects.get_or_create(
            user=user,
        )

        UserSecurity.objects.get_or_create(
            user=user,
        )


        logger.info(
            "Social account initialized.",
            extra={
                "user_id": user.id,
            },
        )

        return user

    @staticmethod
    def update_last_login(user):
        """
        Update user activity.
        """

        activity = user.activity

        activity.status = "online"

        activity.save(
            update_fields=[
                "status",
            ]
        )

    @staticmethod
    def get_provider_name(social_account):
        """
        Return provider name.
        """

        return social_account.provider.capitalize()

    @staticmethod
    def is_social_account(user):
        """
        Check whether user has
        any linked social account.
        """

        return user.socialaccount_set.exists()

    @staticmethod
    def linked_accounts(user):
        """
        Return all linked providers.
        """

        return user.socialaccount_set.all()

    @staticmethod
    def unlink_allowed(user):
        """
        Prevent removing the last
        authentication method.
        """

        return (
            user.has_usable_password()
            or user.socialaccount_set.count() > 1
        )