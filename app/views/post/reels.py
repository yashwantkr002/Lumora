"""
===========================================================
File: app/views/post/reels.py
===========================================================

PURPOSE

Display the reels feed.

Business logic belongs to PostReelsService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from app.services.post.reels import ReelsPostService

logger = logging.getLogger(__name__)


@login_required
def reels(request):
    """
    Display the personalized reels feed.
    """

    # -------------------------------------------------------
    # Load Reels
    # -------------------------------------------------------

    posts = ReelsPostService.get_feed_reels(
        user=request.user,
    )

    # -------------------------------------------------------
    # Pagination
    # -------------------------------------------------------

    paginator = Paginator(
        posts,
        10,
    )

    page_number = request.GET.get(
        "page",
    )

    page_obj = paginator.get_page(
        page_number,
    )

    logger.info(
        "Reels viewed.",
        extra={
            "user_id": request.user.id,
            "page": page_obj.number,
        },
    )

    return render(
        request,
        "post/reels.html",
        {
            "page_obj": page_obj,
            "posts": page_obj.object_list,
        },
    )