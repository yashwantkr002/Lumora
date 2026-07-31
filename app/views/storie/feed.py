import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone

from app.models.story import Story

logger = logging.getLogger(__name__)


@login_required
def feed_story(request):
    """
    Display active stories.
    """

    try:

        stories = (
            Story.objects
            .select_related(
                "user",
                "user__profile",
            )
            .filter(
                expires_at__gt=timezone.now(),
            )
            .order_by(
                "-created_at",
            )
        )

        paginator = Paginator(
            stories,
            20,
        )

        page_number = request.GET.get(
            "page",
        )

        page_obj = paginator.get_page(
            page_number,
        )

        logger.info(
            "Story feed loaded.",
            extra={
                "user_id": request.user.id,
            },
        )

    except Exception:

        logger.exception(
            "Failed to load stories.",
            extra={
                "user_id": request.user.id,
            },
        )

        page_obj = Paginator([], 20).get_page(1)

    return render(
        request,
        "stories/feed.html",
        {
            "page_obj": page_obj,
            "stories": page_obj.object_list,
        },
    )