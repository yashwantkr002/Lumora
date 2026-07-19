"""
===========================================================
File: app/views/post/create.py
===========================================================

PURPOSE

Create a new post.

Business logic belongs to PostCreateService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.forms.post.create_post_form import CreatePostForm
from app.services.post.create import CreatePostService

logger = logging.getLogger(__name__)


@login_required
def create_post(request):
    """
    Create a new post.
    """

    if request.method == "POST":

        form = CreatePostForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            try:

                post = CreatePostService.create_post(
                    author=request.user,
                    cleaned_data=form.cleaned_data,
                    files=request.FILES,
                )

                messages.success(
                    request,
                    "Post created successfully.",
                )

                logger.info(
                    "Post created successfully.",
                    extra={
                        "user_id": request.user.id,
                        "post_id": post.id,
                    },
                )

                return redirect(
                    "post:detail",
                    post_id=post.id,
                )

            except Exception:

                logger.exception(
                    "Failed to create post.",
                    extra={
                        "user_id": request.user.id,
                    },
                )

                messages.error(
                    request,
                    "Unable to create post. Please try again.",
                )

        else:

            messages.error(
                request,
                "Please correct the errors below.",
            )

    else:

        form = CreatePostForm()

    return render(
        request,
        "post/create_post.html",
        {
            "form": form,
        },
    )