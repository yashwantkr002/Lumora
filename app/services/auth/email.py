"""
===========================================================
File: app/services/auth/email.py
===========================================================

PURPOSE

Centralized Email Service.

Only this file should send emails.

All other services (Registration, Password, etc.)
must call this service instead of calling send_mail()
directly.

===========================================================
"""

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class EmailService:
    """
    Handles all outgoing emails.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Centralized send_mail().
    #
    # Every email in the project goes through this method.
    #
    # Benefits
    #
    # • One place for logging
    # • One place for exception handling
    # • Easy to switch to Celery later
    # • Easy to switch SMTP provider
    #
    # -------------------------------------------------------

    @staticmethod
    def send_email(
        *,
        subject: str,
        recipient: str,
        template: str,
        context: dict,
        plain_message: str,
    ) -> bool:

        try:

            html_message = render_to_string(
                template,
                context,
            )

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                html_message=html_message,
                fail_silently=False,
            )

            logger.info(
                "Email sent successfully.",
                extra={
                    "recipient": recipient,
                    "subject": subject,
                },
            )

            return True

        except Exception:

            logger.exception(
                "Failed to send email.",
                extra={
                    "recipient": recipient,
                    "subject": subject,
                },
            )

            return False

    # -------------------------------------------------------
    # FIX #2
    #
    # Welcome Email
    #
    # -------------------------------------------------------

    @staticmethod
    def send_welcome_email(
        *,
        user,
        login_url: str,
    ) -> bool:

        return EmailService.send_email(
            subject="Welcome to Lumora",
            recipient=user.email,
            template="emails/welcome.html",
            context={
                "user": user,
                "login_url": login_url,
            },
            plain_message=(
                "Welcome to Lumora.\n\n"
                "Your account has been created successfully."
            ),
        )

    # -------------------------------------------------------
    # FIX #3
    #
    # Verification Email
    #
    # -------------------------------------------------------

    @staticmethod
    def send_verification_email(
        *,
        user,
        otp: str,
    ) -> bool:

        return EmailService.send_email(
            subject="Verify Your Lumora Account",
            recipient=user.email,
            template="emails/verification.html",
            context={
                "user": user,
                "otp": otp,
            },
            plain_message=f"Your verification code is: {otp}",
        )

    # -------------------------------------------------------
    # FIX #4
    #
    # Password Reset Email
    #
    # -------------------------------------------------------

    @staticmethod
    def send_password_reset_email(
        *,
        user,
        reset_url: str,
    ) -> bool:

        return EmailService.send_email(
            subject="Reset Your Lumora Password",
            recipient=user.email,
            template="emails/password_reset.html",
            context={
                "user": user,
                "reset_url": reset_url,
            },
            plain_message=(
                f"Reset your password:\n\n{reset_url}"
            ),
        )