"""
===========================================================
File: app/urls/save.py
===========================================================

PURPOSE

Bookmark URL configuration.

===========================================================
"""

from django.urls import path

from app.views.save.toggle import (
    toggle_save,
)

app_name = "save"

urlpatterns = [

    # -------------------------------------------------------
    # Toggle Bookmark
    # -------------------------------------------------------

    path(
        "post/<uuid:post_id>/toggle/",
        toggle_save,
        name="toggle",
    ),

]