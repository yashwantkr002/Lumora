"""
===========================================================
File: app/views/post/update.py
===========================================================

PURPOSE

Update an existing post.

Business logic belongs to:

• PostDetailService
• PostUpdateService
• PostPermissionService

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from app.forms.post.update_post_form import UpdatePostForm
from app.services.post.detail import PostDetailService
from app.services.post.permissions import PostPermissionService
from app.services.post.update import UpdatePostService

logger = logging.getLogger(__name__)


@login_required
def update_post(request, post_id):
    """
    Update an existing post.
    """

    try:

        # -------------------------------------------------------
        # Load Post
        # -------------------------------------------------------

        post = PostDetailService.get_post(
            post_id=post_id,
        )

        # -------------------------------------------------------
        # Permission Check
        # -------------------------------------------------------

        PostPermissionService.require_edit_permission(
            post=post,
            user=request.user,
        )

        # -------------------------------------------------------
        # Handle Form Submission
        # -------------------------------------------------------

        if request.method == "POST":

            form = UpdatePostForm(
                request.POST,
                request.FILES,
                instance=post,
            )

            if form.is_valid():

                UpdatePostService.update_post(
                    post=post,
                    user=request.user,
                    cleaned_data=form.cleaned_data,
                    media_files=request.FILES.getlist(
                        "media",
                    ),
                )

                messages.success(
                    request,
                    "Post updated successfully.",
                )

                logger.info(
                    "Post updated.",
                    extra={
                        "post_id": post.id,
                        "user_id": request.user.id,
                    },
                )

                return redirect(
                    "post_detail",
                    post_id=post.id,
                )

            messages.error(
                request,
                "Please correct the errors below.",
            )

        else:

            form = UpdatePostForm(
                instance=post,
            )

        return render(
            request,
            "post/update.html",
            {
                "form": form,
                "post": post,
            },
        )

    except PermissionDenied:

        messages.error(
            request,
            "You do not have permission to edit this post.",
        )

    except Exception:

        logger.exception(
            "Unable to update post.",
            extra={
                "post_id": post_id,
                "user_id": request.user.id,
            },
        )

        messages.error(
            request,
            "Unable to update the post.",
        )

    return redirect(
        "feed",
    )