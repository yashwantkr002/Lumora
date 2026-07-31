"""
===========================================================
File: app/urls/like.py
===========================================================

PURPOSE

Like URL configuration.

===========================================================
"""

from django.urls import path

from app.views.like.toggle import toggle_like

app_name = "like"

urlpatterns = [

    # -------------------------------------------------------
    # Toggle Like
    # -------------------------------------------------------

    path(
        "post/<uuid:post_id>/toggle/",
        toggle_like,
        name="toggle",
    ),

]