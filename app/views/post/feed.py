"""
===========================================================
File: app/views/post/feed.py
===========================================================

PURPOSE

Display the authenticated user's home feed.

Business logic belongs to PostFeedService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from app.services.post.feed import FeedPostService

logger = logging.getLogger(__name__)


@login_required
def feed(request):
    """
    Display the personalized home feed.
    """

    # -------------------------------------------------------
    # Load Feed
    # -------------------------------------------------------

    posts = FeedPostService.get_feed(
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
        "Feed viewed.",
        extra={
            "user_id": request.user.id,
            "page": page_obj.number,
        },
    )

    return render(
        request,
        "post/feed.html",
        {
            "page_obj": page_obj,
            "posts": page_obj.object_list,
        },
    )
