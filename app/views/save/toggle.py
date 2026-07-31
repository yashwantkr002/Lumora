"""
===========================================================
File: app/views/save/toggle.py
===========================================================

PURPOSE

Toggle bookmark for a post.

Business logic belongs to SaveToggleService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.services.post.detail import (
    PostDetailService,
)

from app.services.save.toggle import (
    SaveToggleService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def toggle_save(
    request,
    post_id,
):
    """
    Toggle bookmark for a post.
    """

    try:

        # -------------------------------------------------------
        # Load Post
        # -------------------------------------------------------

        post = PostDetailService.get_post(
            post_id=post_id,
        )

        # -------------------------------------------------------
        # Toggle Bookmark
        # -------------------------------------------------------

        result = (
            SaveToggleService.toggle_save(
                post=post,
                user=request.user,
            )
        )

        logger.info(
            "Bookmark toggled.",
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
            "Unable to toggle bookmark.",
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