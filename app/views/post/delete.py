"""
===========================================================
File: app/views/post/delete.py
===========================================================

PURPOSE

Delete an existing post.

Business logic belongs to:

• PostDetailService
• PostDeleteService
• PostPermissionService

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.post import (
    DeletePostService,
    PostDetailService,
    PostPermissionService,
)


logger = logging.getLogger(__name__)


@login_required
@require_POST
def delete_post(request, post_id):
    """
    Delete an existing post.
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

        PostPermissionService.require_delete_permission(
            post=post,
            user=request.user,
        )

        # -------------------------------------------------------
        # Delete Post
        # -------------------------------------------------------

        DeletePostService.delete_post(
            post=post,
            user=request.user,
        )

        logger.info(
            "Post deleted.",
            extra={
                "post_id": post.id,
                "user_id": request.user.id,
            },
        )

        messages.success(
            request,
            "Post deleted successfully.",
        )

    except PermissionDenied:

        messages.error(
            request,
            "You do not have permission to delete this post.",
        )

    except Exception:

        logger.exception(
            "Unable to delete post.",
            extra={
                "post_id": post_id,
                "user_id": request.user.id,
            },
        )

        messages.error(
            request,
            "Unable to delete the post.",
        )

    return redirect(
        "feed",
    )
