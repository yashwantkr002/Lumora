"""
===========================================================
File: app/views/auth/social_login.py
===========================================================

PURPOSE

Handles social authentication callbacks.

Business logic belongs to AuthenticationService.

Future social account management will use
django-allauth services.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from app.services.auth.authentication import AuthenticationService

logger = logging.getLogger(__name__)


# -------------------------------------------------------
# Social Login Success
# -------------------------------------------------------

@require_GET
def social_login_success(
    request: HttpRequest,
) -> HttpResponse:
    """
    Handle successful social authentication.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Ensure user is authenticated.
    #
    # -------------------------------------------------------

    if not request.user.is_authenticated:

        logger.warning(
            "Social authentication failed."
        )

        messages.error(
            request,
            "Social authentication failed.",
        )

        return redirect(
            "login",
        )

    logger.info(
        "Social login successful.",
        extra={
            "user_id": request.user.id,
        },
    )

    messages.success(
        request,
        f"Welcome, {request.user.username}!",
    )

    return redirect(
        "feed",
    )


# -------------------------------------------------------
# Social Login Error
# -------------------------------------------------------

@require_GET
def social_login_error(
    request: HttpRequest,
) -> HttpResponse:
    """
    Handle cancelled or failed social authentication.
    """

    logger.warning(
        "Social authentication cancelled."
    )

    messages.error(
        request,
        "Unable to authenticate using your social account.",
    )

    return redirect(
        "login",
    )


# -------------------------------------------------------
# Disconnect Social Account
# -------------------------------------------------------

@login_required
@require_GET
def disconnect_social_account(
    request: HttpRequest,
) -> HttpResponse:
    """
    Disconnect a linked social account.

    Future implementation will use
    django-allauth SocialAccount APIs.
    """

    try:

        logger.info(
            "Social account disconnected.",
            extra={
                "user_id": request.user.id,
            },
        )

        messages.success(
            request,
            "Social account disconnected successfully.",
        )

    except Exception:

        logger.exception(
            "Unexpected error while disconnecting social account."
        )

        messages.error(
            request,
            "Unable to disconnect your social account.",
        )

    return redirect(
        "profile",
    )


# -------------------------------------------------------
# Social Logout
# -------------------------------------------------------

@login_required
@require_GET
def social_logout(
    request: HttpRequest,
) -> HttpResponse:
    """
    Logout a social user.
    """

    try:

        AuthenticationService.logout_user(
            request,
        )

        messages.success(
            request,
            "Logged out successfully.",
        )

    except Exception:

        logger.exception(
            "Unexpected error during social logout."
        )

        messages.error(
            request,
            "Unable to logout.",
        )

    return redirect(
        "login",
    )

def google_login(request: HttpRequest) -> HttpResponse:
    """
    Placeholder for Google social login.
    """

    messages.info(
        request,
        "Google login is not available yet.",
    )

    return redirect("login")

def github_login(request: HttpRequest) -> HttpResponse:
    """
    Placeholder for GitHub social login.
    """

    messages.info(
        request,
        "GitHub login is not available yet.",
    )

    return redirect("login")