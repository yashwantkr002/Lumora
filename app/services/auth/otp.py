"""
===========================================================
File: app/services/auth/otp.py
===========================================================

PURPOSE

Handles all OTP related operations.

Only this service should interact with pyotp.

===========================================================
"""

import logging

import pyotp

from app.models.user import UserVerification

logger = logging.getLogger(__name__)


class OTPService:
    """
    Handles OTP generation and verification.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Create a new OTP secret.
    #
    # Used during user registration or when
    # resetting two-factor authentication.
    # -------------------------------------------------------

    @staticmethod
    def generate_secret() -> str:

        return pyotp.random_base32()

    # -------------------------------------------------------
    # FIX #2
    #
    # Generate a 6-digit OTP using the user's secret.
    # -------------------------------------------------------

    @staticmethod
    def generate_otp(user) -> str:

        totp = pyotp.TOTP(
            user.verification.otp_secret
        )

        otp = totp.now()

        logger.info(
            "OTP generated.",
            extra={
                "user_id": user.id,
            },
        )

        return otp

    # -------------------------------------------------------
    # FIX #3
    #
    # Verify OTP entered by the user.
    #
    # valid_window=1 allows a small clock drift.
    # -------------------------------------------------------

    @staticmethod
    def verify_otp(
        user,
        otp: str,
    ) -> bool:

        totp = pyotp.TOTP(
            user.verification.otp_secret
        )

        is_valid = totp.verify(
            otp,
            valid_window=1,
        )

        if is_valid:

            logger.info(
                "OTP verified successfully.",
                extra={
                    "user_id": user.id,
                },
            )

        else:

            logger.warning(
                "Invalid OTP.",
                extra={
                    "user_id": user.id,
                },
            )

        return is_valid

    # -------------------------------------------------------
    # FIX #4
    #
    # Regenerate user's OTP secret.
    #
    # Useful when enabling/disabling 2FA.
    # -------------------------------------------------------

    @staticmethod
    def regenerate_secret(user) -> str:

        secret = OTPService.generate_secret()

        verification = UserVerification.objects.get(
            user=user,
        )

        verification.otp_secret = secret

        verification.save(
            update_fields=[
                "otp_secret",
            ],
        )

        logger.info(
            "OTP secret regenerated.",
            extra={
                "user_id": user.id,
            },
        )

        return secret

    # -------------------------------------------------------
    # FIX #5
    #
    # Generate a fresh OTP.
    #
    # Future:
    # Can be used for "Resend OTP".
    # -------------------------------------------------------

    @staticmethod
    def resend_otp(user) -> str:

        otp = OTPService.generate_otp(user)

        logger.info(
            "OTP regenerated.",
            extra={
                "user_id": user.id,
            },
        )

        return otp