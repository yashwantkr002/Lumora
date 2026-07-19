"""
===========================================================
File: app/views/comment/create.py
===========================================================

PURPOSE

Create a comment.

Business logic belongs to CommentCreateService.

===========================================================
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.forms.comment.comment_form import CommentForm
from app.services.comment.create import (
    CommentCreateService,
)
from app.services.post.detail import (
    PostDetailService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def create_comment(
    request,
    post_id,
):
    """
    Create a comment.
    """

    post = PostDetailService.get_post(
        post_id=post_id,
    )

    form = CommentForm(
        request.POST,
    )

    if not form.is_valid():

        messages.error(
            request,
            "Please correct the errors below.",
        )

        return redirect(
            "post:detail",
            post_id=post.id,
        )

    parent = None

    parent_id = request.POST.get(
        "parent_id",
    )

    if parent_id:

        from app.services.comment.detail import (
            CommentDetailService,
        )

        parent = CommentDetailService.get_comment(
            comment_id=parent_id,
        )

    CommentCreateService.create_comment(
        post=post,
        author=request.user,
        content=form.cleaned_data["content"],
        parent=parent,
    )

    logger.info(
        "Comment created.",
        extra={
            "post_id": post.id,
            "user_id": request.user.id,
        },
    )

    messages.success(
        request,
        "Comment added.",
    )

    return redirect(
        "post:detail",
        post_id=post.id,
    )