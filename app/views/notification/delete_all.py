"""
===========================================================
File: app/views/notification/delete_all.py
===========================================================

PURPOSE

Delete all read notifications.

===========================================================
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from app.services.notification.delete import (
    NotificationDeleteService,
)

logger = logging.getLogger(__name__)


@login_required
@require_POST
def delete_read_notifications(
    request,
):
    """
    Delete all read notifications.
    """

    deleted = (
        NotificationDeleteService
        .delete_read_notifications(
            user=request.user,
        )
    )

    logger.info(
        "Read notifications deleted.",
        extra={
            "user_id": request.user.id,
            "deleted": deleted,
        },
    )

    return redirect(
        "notification:list",
    )