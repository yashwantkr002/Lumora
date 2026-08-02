from app.services.notification.query import NotificationQueryService


def unread_notifications(request):
    if not request.user.is_authenticated:
        return {"unread_notifications_count": 0}

    return {
        "unread_notifications_count": NotificationQueryService.unread_count(user=request.user),
    }
