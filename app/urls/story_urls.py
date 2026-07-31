from django.urls import path

from app.views.storie import(
    delete_story,
    create_story,
    feed_story,
    detail_story,
    next_story,
    previous_story,
    reply_story,
)


urlpatterns = [
    path(
        "",
        feed_story,
        name="feed_story",
    ),
    path(
        "create/",
        create_story,
        name="create_story",
    ),
    path(
        "<uuid:story_id>/",
        detail_story,
        name="detail_story",
    ),
    path(
        "<uuid:story_id>/previous/",
        previous_story,
        name="previous_story",
    ),
    path(
        "<uuid:story_id>/next/",
        next_story,
        name="next_story",
    ),
    path(
        "<uuid:story_id>/reply/",
        reply_story,
        name="reply_story",
    ),
    path(
        "<uuid:story_id>/delete/",
        delete_story,
        name="delete_story",
    ),
]