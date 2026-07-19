"""
===========================================================
File: app/services/auth/authentication.py
===========================================================

PURPOSE

Handles authentication workflow.

Business logic related to Activity and Security
is delegated to dedicated services.

===========================================================
"""

import logging

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)
from django.core.exceptions import ValidationError
from django.db.models import Q

from app.services.auth.activity import ActivityService
from app.services.auth.security import SecurityService

logger = logging.getLogger(__name__)

User = get_user_model()


class AuthenticationService:
    """
    Handles user authentication.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Login user.
    #
    # Flow
    #
    # Find User
    # ↓
    # Check Account Lock
    # ↓
    # Authenticate
    # ↓
    # Reset Failed Attempts
    # ↓
    # Mark Online
    # ↓
    # Login
    #
    # -------------------------------------------------------

    @staticmethod
    def login_user(request, form):

        identifier = form.cleaned_data["username_or_email"].strip()

        password = form.cleaned_data["password"]

        remember_me = form.cleaned_data.get(
            "remember_me",
            False,
        )

        # ---------------------------------------------------
        # FIX #2
        #
        # Find user by username or email.
        #
        # This allows us to perform security checks
        # before authentication.
        #
        # ---------------------------------------------------

        user_obj = User.objects.filter(
            Q(email__iexact=identifier)
            | Q(username__iexact=identifier)
        ).first()

        # ---------------------------------------------------
        # FIX #3
        #
        # If user exists, check account lock.
        #
        # ---------------------------------------------------

        if user_obj:

            if not SecurityService.can_login(user_obj):

                logger.warning(
                    "Blocked login attempt for locked account.",
                    extra={
                        "user_id": user_obj.id,
                    },
                )

                raise ValidationError(
                    "Your account is temporarily locked."
                )

        # ---------------------------------------------------
        # FIX #4
        #
        # Authenticate.
        #
        # NOTE:
        # Until a custom authentication backend is added,
        # authentication will work using USERNAME_FIELD
        # (email in this project).
        #
        # ---------------------------------------------------

        user = authenticate(
            username=identifier,
            password=password,
        )

        # ---------------------------------------------------
        # FIX #5
        #
        # Failed login.
        #
        # Increment failed attempts only if
        # the user actually exists.
        #
        # ---------------------------------------------------

        if user is None:

            if user_obj:

                SecurityService.increment_failed_attempts(
                    user_obj,
                )

                logger.warning(
                    "Failed login attempt.",
                    extra={
                        "user_id": user_obj.id,
                    },
                )

            else:

                logger.warning(
                    "Failed login attempt for unknown account."
                )

            raise ValidationError(
                "Invalid username/email or password."
            )

        # ---------------------------------------------------
        # FIX #6
        #
        # Reset failed attempts.
        #
        # ---------------------------------------------------

        SecurityService.reset_failed_attempts(
            user,
        )

        # ---------------------------------------------------
        # FIX #7
        #
        # Login user.
        #
        # ---------------------------------------------------

        login(
            request,
            user,
        )

        # ---------------------------------------------------
        # FIX #8
        #
        # Mark user online.
        #
        # ---------------------------------------------------

        ActivityService.mark_online(
            user,
        )

        # ---------------------------------------------------
        # FIX #9
        #
        # Remember Me.
        #
        # ---------------------------------------------------

        if remember_me:

            request.session.set_expiry(
                60 * 60 * 24 * 30
            )

        else:

            request.session.set_expiry(0)

        logger.info(
            "User logged in successfully.",
            extra={
                "user_id": user.id,
            },
        )

        return user

    # -------------------------------------------------------
    # FIX #10
    #
    # Logout user.
    #
    # -------------------------------------------------------

    @staticmethod
    def logout_user(request):

        user = request.user

        if user.is_authenticated:

            ActivityService.mark_offline(
                user,
            )

            logger.info(
                "User logged out.",
                extra={
                    "user_id": user.id,
                },
            )

        logout(request)