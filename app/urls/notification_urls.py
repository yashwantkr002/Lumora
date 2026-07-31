"""
===========================================================
File: app/urls/notification.py
===========================================================

PURPOSE

Notification URL configuration.

===========================================================
"""

from django.urls import path

from app.views.notification.delete import (
    delete_notification,
)

from app.views.notification.delete_all import (
    delete_read_notifications,
)

from app.views.notification.list import (
    notification_list,
)

from app.views.notification.mark_all_read import (
    mark_all_notifications_read,
)

from app.views.notification.mark_read import (
    mark_notification_read,
)

app_name = "notification"

urlpatterns = [

    # -------------------------------------------------------
    # Notification List
    # -------------------------------------------------------

    path(
        "",
        notification_list,
        name="list",
    ),

    # -------------------------------------------------------
    # Mark Notification As Read
    # -------------------------------------------------------

    path(
        "<uuid:notification_id>/read/",
        mark_notification_read,
        name="mark_read",
    ),

    # -------------------------------------------------------
    # Mark All Notifications As Read
    # -------------------------------------------------------

    path(
        "read-all/",
        mark_all_notifications_read,
        name="mark_all_read",
    ),

    # -------------------------------------------------------
    # Delete Notification
    # -------------------------------------------------------

    path(
        "<uuid:notification_id>/delete/",
        delete_notification,
        name="delete",
    ),

    # -------------------------------------------------------
    # Delete Read Notifications
    # -------------------------------------------------------

    path(
        "delete-read/",
        delete_read_notifications,
        name="delete_read",
    ),

]