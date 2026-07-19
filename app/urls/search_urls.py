from django.urls import path

from app.views.post.search import search_posts

urlpatterns = [
    path(
        "search/",
        search_posts,
        name="search",
    ),
]
