"""
===========================================================
File: app/views/auth/login.py
===========================================================

PURPOSE

Handles login requests.

Business logic belongs to AuthenticationService.

===========================================================
"""

import logging

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from app.forms.auth.login_form import LoginForm
from app.services.auth.authentication import AuthenticationService

logger = logging.getLogger(__name__)


def user_login(request):
    """
    Authenticate and log in a user.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Redirect authenticated users.
    #
    # -------------------------------------------------------

    if request.user.is_authenticated:
        return redirect("post:feed")

    # -------------------------------------------------------
    # FIX #2
    #
    # Validate next URL to prevent open redirects.
    #
    # -------------------------------------------------------

    next_url = request.GET.get("next") or request.POST.get("next")

    if next_url and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
    ):
        next_url = None

    # -------------------------------------------------------
    # FIX #3
    #
    # Handle POST request.
    #
    # -------------------------------------------------------

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            try:

                # -------------------------------------------
                # AuthenticationService performs:
                #
                # • Authentication
                # • Security checks
                # • Login
                # • Activity update
                #
                # -------------------------------------------

                user = AuthenticationService.login_user(
                    request=request,
                    form=form,
                )

                messages.success(
                    request,
                    f"Welcome back, {user.username}!",
                )

                return redirect(next_url or "post:feed")

            # -----------------------------------------------
            # FIX #4
            #
            # Show validation messages.
            #
            # -----------------------------------------------

            except ValidationError as exc:

                messages.error(
                    request,
                    exc.message,
                )

            # -----------------------------------------------
            # FIX #5
            #
            # Unexpected server error.
            #
            # -----------------------------------------------

            except Exception:

                logger.exception(
                    "Unexpected login error."
                )

                messages.error(
                    request,
                    "Something went wrong. Please try again.",
                )

        else:

            messages.error(
                request,
                "Please correct the errors below.",
            )

    else:

        form = LoginForm()

    # -------------------------------------------------------
    # FIX #6
    #
    # Render login page.
    #
    # -------------------------------------------------------

    return render(
        request,
        "auth/login.html",
        {
            "form": form,
            "next": next_url,
        },
    )

