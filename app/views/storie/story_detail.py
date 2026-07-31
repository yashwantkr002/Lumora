import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.services.storie.detail import DetailStoryService

logger = logging.getLogger(__name__)


@login_required
def detail_story(request, story_id):
    """
    Display a single story.
    """

    try:
        story = DetailStoryService.get_story(story_id=story_id)

        if story.is_expired:
            messages.error(request, "This story has expired.")
            return redirect("story_feed")

        logger.info(
            "Story detail viewed.",
            extra={
                "story_id": story.id,
                "user_id": request.user.id,
            },
        )

        return render(
            request,
            "stories/story_detail.html",
            {
                "story": story,
            },
        )

    except Exception:
        logger.exception(
            "Unable to load story.",
            extra={
                "story_id": story_id,
                "user_id": request.user.id,
            },
        )

        messages.error(request, "Story not found.")
        return redirect("story_feed")


@login_required
def previous_story(request, story_id):
    """
    Redirect to the previous active story in the feed order.
    """

    try:
        story = DetailStoryService.get_story(story_id=story_id)
        stories = list(DetailStoryService.get_active_stories())
        current_index = next(
            (
                index
                for index, candidate in enumerate(stories)
                if candidate.id == story.id
            ),
            None,
        )

        if current_index is None or current_index >= len(stories) - 1:
            return redirect("story_feed")

        return redirect("story_detail", story_id=stories[current_index + 1].id)

    except Exception:
        return redirect("story_feed")


@login_required
def next_story(request, story_id):
    """
    Redirect to the next active story in the feed order.
    """

    try:
        story = DetailStoryService.get_story(story_id=story_id)
        stories = list(DetailStoryService.get_active_stories())
        current_index = next(
            (
                index
                for index, candidate in enumerate(stories)
                if candidate.id == story.id
            ),
            None,
        )

        if current_index is None or current_index <= 0:
            return redirect("story_feed")

        return redirect("story_detail", story_id=stories[current_index - 1].id)

    except Exception:
        return redirect("story_feed")


@login_required
def reply_story(request, story_id):
    """
    Handle story replies by redirecting back to the story detail view.
    """

    return redirect("story_detail", story_id=story_id)
