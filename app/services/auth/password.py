"""
===========================================================
File: app/services/auth/password.py
===========================================================

PURPOSE

Handles password reset and password change operations.

This service DOES NOT

• send emails
• render templates
• call send_mail()

Those responsibilities belong to EmailService.

===========================================================
"""

import logging

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.services.auth.email import EmailService

logger = logging.getLogger(__name__)


class PasswordService:
    """
    Handles password related operations.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Generate password reset link and delegate
    # email sending to EmailService.
    # -------------------------------------------------------

    @staticmethod
    def send_password_reset_email(
        user,
        request,
    ) -> bool:

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(
            user
        )

        reset_url = request.build_absolute_uri(
            reverse(
                "reset_password",
                kwargs={
                    "uidb64": uid,
                    "token": token,
                },
            )
        )

        success = EmailService.send_password_reset_email(
            user=user,
            reset_url=reset_url,
        )

        if success:

            logger.info(
                "Password reset email sent.",
                extra={
                    "user_id": user.id,
                },
            )

        else:

            logger.exception(
                "Failed to send password reset email.",
                extra={
                    "user_id": user.id,
                },
            )

        return success

    # -------------------------------------------------------
    # FIX #2
    #
    # Reset user password.
    #
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def reset_password(
        user,
        password,
        request=None,
    ) -> bool:

        validate_password(
            password,
            user,
        )

        user.set_password(
            password,
        )

        user.save(
            update_fields=[
                "password",
            ],
        )

        if request is not None:

            update_session_auth_hash(
                request,
                user,
            )

        logger.info(
            "Password reset completed.",
            extra={
                "user_id": user.id,
            },
        )

        return True

    # -------------------------------------------------------
    # FIX #3
    #
    # Change password.
    #
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def change_password(
        user,
        old_password,
        new_password,
        request=None,
    ) -> bool:

        if not user.check_password(
            old_password,
        ):

            raise ValueError(
                "Current password is incorrect."
            )

        validate_password(
            new_password,
            user,
        )

        user.set_password(
            new_password,
        )

        user.save(
            update_fields=[
                "password",
            ],
        )

        if request is not None:

            update_session_auth_hash(
                request,
                user,
            )

        logger.info(
            "Password changed.",
            extra={
                "user_id": user.id,
            },
        )

        return True

    # -------------------------------------------------------
    # FIX #4
    #
    # Verify password reset token.
    #
    # -------------------------------------------------------

    @staticmethod
    def verify_token(
        user,
        token,
    ) -> bool:

        return default_token_generator.check_token(
            user,
            token,
        )