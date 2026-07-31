"""
===========================================================
File: app/views/comment/delete.py
===========================================================

PURPOSE

Delete a comment.

Business logic belongs to CommentDeleteService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.comment.delete import (
    CommentDeleteService,
)
from app.services.comment.detail import (
    CommentDetailService,
)
from app.services.comment.permissions import (
    CommentPermissionService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def delete_comment(
    request,
    comment_id,
):
    """
    Delete a comment.
    """

    comment = None

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

        CommentPermissionService.require_delete_permission(
            comment=comment,
            user=request.user,
        )

        # -------------------------------------------------------
        # Delete
        # -------------------------------------------------------

        CommentDeleteService.delete_comment(
            comment=comment,
            user=request.user,
        )

        logger.info(
            "Comment deleted.",
            extra={
                "comment_id": comment.id,
                "user_id": request.user.id,
            },
        )

        messages.success(
            request,
            "Comment deleted successfully.",
        )

    except PermissionDenied:

        messages.error(
            request,
            "You do not have permission to delete this comment.",
        )

    except Exception:

        logger.exception(
            "Unable to delete comment.",
            extra={
                "comment_id": comment_id,
                "user_id": request.user.id,
            },
        )

        messages.error(
            request,
            "Unable to delete comment.",
        )

    if comment:

        return redirect(
            "post:detail",
            post_id=comment.post.id,
        )

    return redirect(
        "post:feed",
    )