"""
===========================================================
File: app/views/notification/list.py
===========================================================

PURPOSE

Display the user's notifications.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.services.notification.query import (
    NotificationQueryService,
)

logger = logging.getLogger(__name__)


@login_required
def notification_list(
    request,
):
    """
    Display notifications for the current user.
    """

    notifications = (
        NotificationQueryService
        .user_queryset(
            user=request.user,
        )
    )

    unread_count = (
        NotificationQueryService
        .unread_count(
            user=request.user,
        )
    )

    logger.info(
        "Notification list loaded.",
        extra={
            "user_id": request.user.id,
        },
    )

    return render(
        request,
        "notifications/list.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
        },
    )