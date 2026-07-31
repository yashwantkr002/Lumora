"""
===========================================================
File: app/services/auth/security.py
===========================================================

PURPOSE

Handles account security.

Only this service should update UserSecurity.

===========================================================
"""

import logging
from datetime import timedelta

from django.utils import timezone

from app.models.user import UserSecurity

logger = logging.getLogger(__name__)


class SecurityService:
    """
    Handles account security operations.
    """

    MAX_FAILED_ATTEMPTS = 5
    LOCK_DURATION_MINUTES = 30

    # -------------------------------------------------------
    # FIX #1
    #
    # Get or create security record.
    #
    # Prevents RelatedObjectDoesNotExist.
    #
    # -------------------------------------------------------

    @staticmethod
    def get_security(user) -> UserSecurity:

        security, _ = UserSecurity.objects.get_or_create(
            user=user,
        )

        return security

    # -------------------------------------------------------
    # FIX #2
    #
    # Increase failed login attempts.
    #
    # Automatically lock account after limit.
    #
    # -------------------------------------------------------

    @staticmethod
    def increment_failed_attempts(user) -> None:

        security = SecurityService.get_security(user)

        security.failed_login_attempts += 1

        if (
            security.failed_login_attempts
            >= SecurityService.MAX_FAILED_ATTEMPTS
        ):

            security.account_locked_until = (
                timezone.now()
                + timedelta(
                    minutes=SecurityService.LOCK_DURATION_MINUTES
                )
            )

            logger.warning(
                "Account locked due to too many failed login attempts.",
                extra={
                    "user_id": user.id,
                },
            )

        security.save(
            update_fields=[
                "failed_login_attempts",
                "account_locked_until",
            ],
        )

    # -------------------------------------------------------
    # FIX #3
    #
    # Reset failed attempts after successful login.
    #
    # -------------------------------------------------------

    @staticmethod
    def reset_failed_attempts(user) -> None:

        security = SecurityService.get_security(user)

        security.failed_login_attempts = 0
        security.account_locked_until = None

        security.save(
            update_fields=[
                "failed_login_attempts",
                "account_locked_until",
            ],
        )

    # -------------------------------------------------------
    # FIX #4
    #
    # Lock account manually.
    #
    # -------------------------------------------------------

    @staticmethod
    def lock_account(
        user,
        minutes: int = LOCK_DURATION_MINUTES,
    ) -> None:

        security = SecurityService.get_security(user)

        security.account_locked_until = (
            timezone.now()
            + timedelta(
                minutes=minutes,
            )
        )

        security.save(
            update_fields=[
                "account_locked_until",
            ],
        )

        logger.warning(
            "Account manually locked.",
            extra={
                "user_id": user.id,
            },
        )

    # -------------------------------------------------------
    # FIX #5
    #
    # Unlock account.
    #
    # -------------------------------------------------------

    @staticmethod
    def unlock_account(user) -> None:

        security = SecurityService.get_security(user)

        security.failed_login_attempts = 0
        security.account_locked_until = None

        security.save(
            update_fields=[
                "failed_login_attempts",
                "account_locked_until",
            ],
        )

        logger.info(
            "Account unlocked.",
            extra={
                "user_id": user.id,
            },
        )

    # -------------------------------------------------------
    # FIX #6
    #
    # Check whether account is locked.
    #
    # -------------------------------------------------------

    @staticmethod
    def is_account_locked(user) -> bool:

        security = SecurityService.get_security(user)

        if (
            security.account_locked_until
            and timezone.now()
            < security.account_locked_until
        ):
            return True

        return False

    # -------------------------------------------------------
    # FIX #7
    #
    # Check if login is allowed.
    #
    # Future:
    # Add IP restriction
    # Add device verification
    # Add 2FA
    #
    # -------------------------------------------------------

    @staticmethod
    def can_login(user) -> bool:

        return not SecurityService.is_account_locked(
            user,
        )