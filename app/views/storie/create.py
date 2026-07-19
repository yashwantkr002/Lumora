import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from app.forms.storie.story_form import StoryForm as CreateStoryForm
from app.services.storie.create import CreateStoryService

logger = logging.getLogger(__name__)


@login_required
def create_story(request):
    """
    Create a new story.
    """

    if request.method == "POST":

        form = CreateStoryForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            try:

                CreateStoryService.create_story(
                    user=request.user,
                    cleaned_data=form.cleaned_data,
                    files=request.FILES,
                )

                messages.success(
                    request,
                    "Story created successfully.",
                )

                return redirect(
                    "story_feed",
                )

            except ValidationError as e:

                messages.error(
                    request,
                    str(e),
                )
            except Exception as e:
                logger.exception(
                    "Story creation failed.",
                    extra={
                        "user_id": request.user.id,
                    },
                )
                messages.error(
                    request,
                    "Unable to create story.",
                )

    else:

        form = CreateStoryForm()

    return render(
        request,
        "stories/create.html",
        {
            "form": form,
        },
    )
