import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.storie.delete import DeleteStoryService
from app.models.story import Story

logger = logging.getLogger(__name__)


@login_required
@require_POST
def delete_story(request, story_id):
    """
    Delete an existing story.
    """

    try:

        story = Story.objects.get(
            id=story_id,
        )

        DeleteStoryService.delete_story(
            story=story,
            user=request.user,
        )

        messages.success(
            request,
            "Story deleted successfully.",
        )

    except Story.DoesNotExist:

        messages.error(
            request,
            "Story not found.",
        )

    except PermissionDenied:

        messages.error(
            request,
            "You do not have permission to delete this story.",
        )

    except Http404:

        messages.error(
            request,
            "Story not found.",
        )

    except Exception:

        logger.exception(
            "Story deletion failed.",
            extra={
                "story_id": story_id,
                "user_id": request.user.id,
            },
        )

        messages.error(
            request,
            "Unable to delete story.",
        )

    return redirect(
        "story_feed",
    )