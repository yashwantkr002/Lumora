"""
===========================================================
File: app/views/like/toggle.py
===========================================================

PURPOSE

Toggle a like on a post.

Business logic belongs to LikeToggleService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.services.like.toggle import (
    LikeToggleService,
)
from app.services.post.detail import (
    PostDetailService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def toggle_like(
    request,
    post_id,
):
    """
    Toggle like for a post.
    """

    try:

        # -------------------------------------------------------
        # Load Post
        # -------------------------------------------------------

        post = PostDetailService.get_post(
            post_id=post_id,
        )

        # -------------------------------------------------------
        # Toggle Like
        # -------------------------------------------------------

        result = (
            LikeToggleService
            .toggle_like(
                post=post,
                user=request.user,
            )
        )

        logger.info(
            "Like toggled.",
            extra={
                "post_id": post.id,
                "user_id": request.user.id,
            },
        )

        return JsonResponse(
            {
                "success": True,
                **result,
            }
        )

    except Exception:

        logger.exception(
            "Unable to toggle like.",
            extra={
                "post_id": post_id,
                "user_id": request.user.id,
            },
        )

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Unable to process request."
                ),
            },
            status=400,
        )