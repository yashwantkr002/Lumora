"""
===========================================================
File: app/views/notification/delete.py
===========================================================

PURPOSE

Delete a notification.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.notification.query import (
    NotificationQueryService,
)

from app.services.notification.delete import (
    NotificationDeleteService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def delete_notification(
    request,
    notification_id,
):
    """
    Delete a notification.
    """

    notification = (
        NotificationQueryService
        .get_notification(
            notification_id=notification_id,
        )
    )

    NotificationDeleteService.delete_notification(
        notification=notification,
        user=request.user,
    )

    logger.info(
        "Notification deleted.",
        extra={
            "notification_id": notification.id,
            "user_id": request.user.id,
        },
    )

    return redirect(
        "notification:list",
    )