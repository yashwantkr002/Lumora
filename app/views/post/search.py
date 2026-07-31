"""
===========================================================
File: app/views/post/search.py
===========================================================

PURPOSE

Search posts.

Business logic belongs to PostSearchService.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from app.services.post.search import SearchPostService

logger = logging.getLogger(__name__)


@login_required
def search_posts(request):
    """
    Search posts.
    """

    # -------------------------------------------------------
    # Get Query
    # -------------------------------------------------------

    query = (
        request.GET.get(
            "q",
            "",
        )
        .strip()
    )

    # -------------------------------------------------------
    # Search
    # -------------------------------------------------------

    posts = SearchPostService.search_posts(
        query=query,
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
        "Post search executed.",
        extra={
            "user_id": request.user.id,
            "query": query,
            "page": page_obj.number,
        },
    )

    return render(
        request,
        "post/search.html",
        {
            "query": query,
            "page_obj": page_obj,
            "posts": page_obj.object_list,
        },
    )