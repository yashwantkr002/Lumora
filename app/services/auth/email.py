"""
===========================================================
File: app/services/auth/email.py

PURPOSE
Centralized Email Service.
Only this file should send emails.
===========================================================
"""

import logging
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class EmailService:
    """
    Handles all outgoing emails.
    """

    @staticmethod
    def _send_email_task(
        subject: str,
        recipient: str,
        template: str,
        context: dict,
        plain_message: str,
    ) -> None:
        """
        Internal worker method executed in a separate thread.
        Handles template rendering and SMTP execution off the main request thread.
        """
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

        except Exception:
            logger.exception(
                "Failed to send email.",
                extra={
                    "recipient": recipient,
                    "subject": subject,
                },
            )

    @staticmethod
    def send_email(
        *,
        subject: str,
        recipient: str,
        template: str,
        context: dict,
        plain_message: str,
    ) -> bool:
        """
        Dispatches email sending to a background thread to prevent
        SMTP network delays from blocking Gunicorn workers.
        """
        try:
            # Fires the email dispatch in a background thread
            thread = threading.Thread(
                target=EmailService._send_email_task,
                kwargs={
                    "subject": subject,
                    "recipient": recipient,
                    "template": template,
                    "context": context,
                    "plain_message": plain_message,
                },
                daemon=True,  # Daemon thread automatically cleans up
            )
            thread.start()
            return True

        except Exception:
            logger.exception(
                "Failed to dispatch email thread.",
                extra={
                    "recipient": recipient,
                    "subject": subject,
                },
            )
            return False

    # -------------------------------------------------------
    # Welcome Email
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
    # Verification Email
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
    # Password Reset Email
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