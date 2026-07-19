"""
===========================================================
File: app/services/auth/registration.py
===========================================================

PURPOSE

Handles complete user registration workflow.

This service only orchestrates registration.

It does NOT

• send emails
• generate OTP
• render templates

Those responsibilities belong to dedicated services.

===========================================================
"""

import logging

from django.db import transaction
from django.urls import reverse

from app.models.user import (
    CustomUser,
    UserActivity,
    UserProfile,
    UserSecurity,
    UserVerification,
)

from app.services.auth.email import EmailService
from app.services.auth.otp import OTPService

logger = logging.getLogger(__name__)


class RegistrationService:
    """
    Handles complete registration workflow.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Registration orchestrator.
    #
    # -------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def register_user(
        request,
        form,
    ):

        cleaned = form.cleaned_data

        user = CustomUser.objects.create_user(
            username=cleaned["username"],
            email=cleaned["email"],
            first_name=cleaned["first_name"],
            last_name=cleaned["last_name"],
            password=cleaned["password"],
        )

        RegistrationService._create_profile(user)

        RegistrationService._create_verification(user)

        RegistrationService._create_activity(user)

        RegistrationService._create_security(user)

        # ---------------------------------------------
        # FIX #2
        #
        # Generate login URL.
        #
        # ---------------------------------------------

        login_url = request.build_absolute_uri(
            reverse("login")
        )

        # ---------------------------------------------
        # FIX #3
        #
        # Welcome Email
        #
        # ---------------------------------------------

        EmailService.send_welcome_email(
            user=user,
            login_url=login_url,
        )

        # ---------------------------------------------
        # FIX #4
        #
        # Verification Email
        #
        # ---------------------------------------------

        otp = OTPService.generate_otp(user)

        EmailService.send_verification_email(
            user=user,
            otp=otp,
        )

        logger.info(
            "New user registered.",
            extra={
                "user_id": user.id,
            },
        )

        return user

    # -------------------------------------------------------
    # FIX #5
    #
    # Private helper methods.
    #
    # -------------------------------------------------------

    @staticmethod
    def _create_profile(user):

        UserProfile.objects.create(
            user=user,
        )

    @staticmethod
    def _create_verification(user):

        UserVerification.objects.create(
            user=user,
            otp_secret=OTPService.generate_secret(),
        )

    @staticmethod
    def _create_activity(user):

        UserActivity.objects.create(
            user=user,
        )

    @staticmethod
    def _create_security(user):

        UserSecurity.objects.create(
            user=user,
        )