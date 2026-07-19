"""
URL configuration for Lumora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # -------------------------------------------------------
    #    This is the main URL 
    # -------------------------------------------------------
    path("", include("app.urls.auth_urls")),
    # ------------------------------------------------------
    path("posts/", include("app.urls.post_urls")),
    path("chat/", include("app.urls.chat_urls")),
    path("story/", include(("app.urls.story_urls", "story"), namespace="story")),
    path("profiles/", include("app.urls.profile_urls")),
    path("comments/", include("app.urls.comment_urls")),
    path("likes/", include("app.urls.like_urls")),
    path("saves/", include("app.urls.save_urls")),
    path("search/", include("app.urls.search_urls")),
    path("messages/", include("app.urls.message_urls")),
    path("notifications/", include("app.urls.notification_urls")),
    path("__reload__/", include("django_browser_reload.urls"))

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

# +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


