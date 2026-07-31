"""
===========================================================
File: app/views/post/detail.py
===========================================================

PURPOSE

Display a single post.

Business logic belongs to:

• PostDetailService
• PostPermissionService

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from app.services.post.detail import PostDetailService
from app.services.post.permissions import PostPermissionService

logger = logging.getLogger(__name__)


@login_required
def post_detail(request, post_id):
    """
    Display a single post.
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

        PostPermissionService.require_view_permission(
            post=post,
            user=request.user,
        )

        logger.info(
            "Post detail viewed.",
            extra={
                "user_id": request.user.id,
                "post_id": post.id,
            },
        )

        return render(
            request,
            "post/post_detail.html",
            {
                "post": post,
            },
        )

    except PermissionDenied:

        messages.error(
            request,
            "You do not have permission to view this post.",
        )

        return redirect(
            "post:post:feed",
        )

    except Exception:

        logger.exception(
            "Unable to load post.",
            extra={
                "user_id": request.user.id,
                "post_id": post_id,
            },
        )

        messages.error(
            request,
            "Unable to load the requested post.",
        )

        return redirect(
            "feed",
        )