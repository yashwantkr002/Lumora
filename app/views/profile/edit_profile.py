"""
===========================================================
File: app/views/profile/edit_profile.py
===========================================================

PURPOSE

Update the authenticated user's profile.

Business logic belongs to ProfileService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from app.forms.profile.edit_profile_form import EditProfileForm
from app.services.profile.profile import ProfileService

logger = logging.getLogger(__name__)


@login_required
def edit_profile(request):
    """
    Update the authenticated user's profile.
    """

    profile = request.user.profile

    if request.method == "POST":

        form = EditProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():

            try:

                # -------------------------------------------------------
                # FIX #1
                #
                # Delegate profile update to ProfileService.
                #
                # -------------------------------------------------------

                ProfileService.update_profile(
                    profile=profile,
                    cleaned_data=form.cleaned_data,
                    files=request.FILES,
                )

                logger.info(
                    "Profile updated successfully.",
                    extra={
                        "user_id": request.user.id,
                    },
                )

                messages.success(
                    request,
                    "Profile updated successfully.",
                )

                return redirect(
                    "profile",
                    username=request.user.username,
                )

            # -------------------------------------------------------
            # FIX #2
            #
            # Handle business validation errors.
            #
            # -------------------------------------------------------

            except ValidationError as exc:

                messages.error(
                    request,
                    exc.message,
                )

            # -------------------------------------------------------
            # FIX #3
            #
            # Handle unexpected errors.
            #
            # -------------------------------------------------------

            except Exception:

                logger.exception(
                    "Unexpected error while updating profile.",
                )

                messages.error(
                    request,
                    "Unable to update profile.",
                )

        else:

            messages.error(
                request,
                "Please correct the errors below.",
            )

    else:

        form = EditProfileForm(
            instance=profile,
        )

    return render(
        request,
        "profile/edit_profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )