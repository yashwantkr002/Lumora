"""
===========================================================
File: app/views/notification/mark_all_read.py
===========================================================

PURPOSE

Mark all notifications as read.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.notification.read import (
    NotificationReadService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def mark_all_notifications_read(
    request,
):
    """
    Mark all notifications as read.
    """

    updated = (
        NotificationReadService
        .mark_all_as_read(
            user=request.user,
        )
    )

    logger.info(
        "All notifications marked as read.",
        extra={
            "user_id": request.user.id,
            "updated": updated,
        },
    )

    return redirect(
        "notification:list",
    )