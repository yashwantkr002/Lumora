"""
===========================================================
File: app/views/notification/mark_read.py
===========================================================

PURPOSE

Mark a notification as read.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.notification.query import (
    NotificationQueryService,
)

from app.services.notification.read import (
    NotificationReadService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def mark_notification_read(
    request,
    notification_id,
):
    """
    Mark a notification as read.
    """

    notification = (
        NotificationQueryService
        .get_notification(
            notification_id=notification_id,
        )
    )

    NotificationReadService.mark_as_read(
        notification=notification,
    )

    logger.info(
        "Notification marked as read.",
        extra={
            "notification_id": notification.id,
            "user_id": request.user.id,
        },
    )

    return redirect(
        "notification:list",
    )