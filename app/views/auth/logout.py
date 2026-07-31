"""
===========================================================
File: app/views/auth/logout.py
===========================================================

PURPOSE

Handles user logout.

Business logic belongs to AuthenticationService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from app.services.auth.authentication import AuthenticationService

logger = logging.getLogger(__name__)


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logout the authenticated user.
    """

    try:

        # -------------------------------------------------------
        # FIX #1
        #
        # AuthenticationService handles:
        #
        # • Mark user offline
        # • Destroy authentication session
        # • Logging
        #
        # -------------------------------------------------------

        AuthenticationService.logout_user(
            request,
        )

        messages.success(
            request,
            "You have been logged out successfully.",
        )

    # -------------------------------------------------------
    # FIX #2
    #
    # Log unexpected logout failures.
    #
    # -------------------------------------------------------

    except Exception:

        logger.exception(
            "Unexpected error occurred during logout."
        )

        messages.error(
            request,
            "Unable to logout. Please try again.",
        )

    return redirect(
        "login",
    )