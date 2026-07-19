"""
===========================================================
File: app/views/auth/register.py
===========================================================

PURPOSE

Handles user registration requests.

Business logic belongs to RegistrationService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from app.forms.auth.register_form import RegisterForm
from app.services.auth.registration import RegistrationService

logger = logging.getLogger(__name__)


def register_view(request):
    """
    Register a new user.
    """

    # -------------------------------------------------------
    # FIX #1
    #
    # Prevent authenticated users from accessing
    # the registration page.
    #
    # -------------------------------------------------------

    if request.user.is_authenticated:
        return redirect("post:feed")

    # -------------------------------------------------------
    # FIX #2
    #
    # Handle registration form submission.
    #
    # -------------------------------------------------------

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            try:

                # ---------------------------------------------------
                # FIX #3
                #
                # RegistrationService handles:
                #
                # • User creation
                # • Profile creation
                # • Verification record
                # • Activity record
                # • Security record
                # • Welcome email
                # • Verification email
                #
                # ---------------------------------------------------

                user = RegistrationService.register_user(
                    request=request,
                    form=form,
                )

                # ---------------------------------------------------
                # FIX #4
                #
                # Automatically log the user in.
                #
                # ---------------------------------------------------

                login(
                    request,
                    user,
                )

                messages.success(
                    request,
                    "Account created successfully. Welcome to Lumora!",
                )

                return redirect("post:feed")

            # -------------------------------------------------------
            # FIX #5
            #
            # Business validation errors.
            #
            # -------------------------------------------------------

            except ValidationError as exc:

                messages.error(
                    request,
                    exc.message,
                )

            # -------------------------------------------------------
            # FIX #6
            #
            # Unexpected server errors.
            #
            # -------------------------------------------------------

            except Exception:

                logger.exception(
                    "Unexpected error occurred during registration."
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

        form = RegisterForm()

    # -------------------------------------------------------
    # FIX #7
    #
    # Render registration page.
    #
    # -------------------------------------------------------

    return render(
        request,
        "auth/register.html",
        {
            "form": form,
        },
    )