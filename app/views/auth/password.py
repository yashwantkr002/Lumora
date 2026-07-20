"""
===========================================================
File: app/views/auth/password.py
===========================================================

PURPOSE

Handles password reset workflow.

Business logic belongs to PasswordService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django_ratelimit.decorators import ratelimit

from app.forms.auth.forgot_password_form import ForgotPasswordForm
from app.forms.auth.reset_password_form import ResetPasswordForm
from app.services.auth.password import PasswordService

logger = logging.getLogger(__name__)

User = get_user_model()


# -------------------------------------------------------
# Forgot Password
# -------------------------------------------------------

@ratelimit(
    key="ip",
    rate="5/m",
    block=False,
)
def forgot_password(
    request: HttpRequest,
) -> HttpResponse:
    """
    Send password reset email.
    """

    if request.user.is_authenticated:
        return redirect("post:feed")

    # ---------------------------------------------------
    # FIX #1
    #
    # Rate limit.
    #
    # ---------------------------------------------------

    if getattr(request, "limited", False):

        logger.warning(
            "Password reset rate limit exceeded."
        )

        messages.error(
            request,
            "Too many requests. Please try again later.",
        )

        return redirect("login")

    if request.method == "POST":

        form = ForgotPasswordForm(
            request.POST,
        )

        if form.is_valid():

            email = form.cleaned_data["email"]

            try:

                user = User.objects.filter(
                    email__iexact=email,
                ).first()

                # ---------------------------------------
                # FIX #2
                #
                # Prevent user enumeration.
                #
                # ---------------------------------------

                if user:

                    PasswordService.send_password_reset_email(
                        user=user,
                        request=request,
                    )

                    logger.info(
                        "Password reset email sent.",
                        extra={
                            "user_id": user.id,
                        },
                    )

                messages.success(
                    request,
                    (
                        "If an account exists with this email, "
                        "a password reset link has been sent."
                    ),
                )

                return redirect("login")

            except Exception:

                logger.exception(
                    "Failed to process password reset request."
                )

                messages.error(
                    request,
                    "Something went wrong. Please try again.",
                )

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        "auth/forgot_password.html",
        {
            "form": form,
        },
    )


# -------------------------------------------------------
# Reset Password
# -------------------------------------------------------

def reset_password(
    request: HttpRequest,
    uidb64: str,
    token: str,
) -> HttpResponse:
    """
    Reset password using secure token.
    """

    try:

        uid = urlsafe_base64_decode(
            uidb64,
        ).decode()

        user = User.objects.get(
            pk=uid,
        )

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
    ):

        user = None

    # ---------------------------------------------------
    # FIX #3
    #
    # Validate token.
    #
    # ---------------------------------------------------

    if (
        user is None
        or not PasswordService.verify_token(
            user,
            token,
        )
    ):

        logger.warning(
            "Invalid password reset token."
        )

        messages.error(
            request,
            "The password reset link is invalid or expired.",
        )

        return redirect("login")

    if request.method == "POST":

        form = ResetPasswordForm(
            request.POST,
        )

        if form.is_valid():

            try:

                # ---------------------------------------
                # FIX #4
                #
                # Correct field name.
                #
                # ---------------------------------------

                PasswordService.reset_password(
                    user=user,
                    password=form.cleaned_data["new_password"],
                )

                messages.success(
                    request,
                    "Your password has been reset successfully.",
                )

                return redirect("login")

            except ValidationError as exc:

                messages.error(
                    request,
                    exc.message,
                )

            except Exception:

                logger.exception(
                    "Password reset failed."
                )

                messages.error(
                    request,
                    "Something went wrong. Please try again.",
                )

    else:

        form = ResetPasswordForm()

    return render(
        request,
        "auth/reset_password.html",
        {
            "form": form,
        },
    )


# -------------------------------------------------------
# Placeholder
# -------------------------------------------------------

def change_password(
    request: HttpRequest,
) -> HttpResponse:
    """
    Placeholder for authenticated password change.
    """

    messages.info(
        request,
        "Password change is not available yet.",
    )

    return redirect("login")


# -------------------------------------------------------
# Compatibility Wrappers
# -------------------------------------------------------

def resetpass(
    request: HttpRequest,
) -> HttpResponse:

    return forgot_password(
        request,
    )


def passwordResetEmail(
    request: HttpRequest,
) -> HttpResponse:

    return forgot_password(
        request,
    )


def verify_reset_token(
    request: HttpRequest,
    uidb64: str,
    token: str,
) -> HttpResponse:

    return reset_password(
        request,
        uidb64,
        token,
    )


def resend_reset_email(
    request: HttpRequest,
) -> HttpResponse:

    return redirect(
        "forgot_password",
    )