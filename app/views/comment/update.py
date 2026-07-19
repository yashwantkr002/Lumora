"""
===========================================================
File: app/views/comment/update.py
===========================================================

PURPOSE

Update an existing comment.

Business logic belongs to CommentUpdateService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from app.forms.comment.comment_form import CommentForm

from app.services.comment.detail import (
    CommentDetailService,
)
from app.services.comment.permissions import (
    CommentPermissionService,
)
from app.services.comment.update import (
    CommentUpdateService,
)

logger = logging.getLogger(__name__)


@login_required
def update_comment(
    request,
    comment_id,
):
    """
    Update an existing comment.
    """

    try:

        # -------------------------------------------------------
        # Load Comment
        # -------------------------------------------------------

        comment = CommentDetailService.get_comment(
            comment_id=comment_id,
        )

        # -------------------------------------------------------
        # Permission
        # -------------------------------------------------------

        CommentPermissionService.require_edit_permission(
            comment=comment,
            user=request.user,
        )

        # -------------------------------------------------------
        # Handle Form
        # -------------------------------------------------------

        if request.method == "POST":

            form = CommentForm(
                request.POST,
                instance=comment,
            )

            if form.is_valid():

                CommentUpdateService.update_comment(
                    comment=comment,
                    user=request.user,
                    content=form.cleaned_data[
                        "content"
                    ],
                )

                messages.success(
                    request,
                    "Comment updated successfully.",
                )

                logger.info(
                    "Comment updated.",
                    extra={
                        "comment_id": comment.id,
                        "user_id": request.user.id,
                    },
                )

                return redirect(
                    "post:detail",
                    post_id=comment.post.id,
                )

            messages.error(
                request,
                "Please correct the errors below.",
            )

        else:

            form = CommentForm(
                instance=comment,
            )

        return render(
            request,
            "comment/update.html",
            {
                "form": form,
                "comment": comment,
            },
        )

    except PermissionDenied:

        messages.error(
            request,
            "You do not have permission to edit this comment.",
        )

    except Exception:

        logger.exception(
            "Unable to update comment.",
            extra={
                "comment_id": comment_id,
                "user_id": request.user.id,
            },
        )

        messages.error(
            request,
            "Unable to update comment.",
        )

    return redirect(
        "post:detail",
        post_id=comment.post.id,
    )