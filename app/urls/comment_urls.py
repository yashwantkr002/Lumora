"""
===========================================================
File: app/urls/comment.py
===========================================================

PURPOSE

Comment URL configuration.

===========================================================
"""

from django.urls import path

from app.views.comment.create import create_comment
from app.views.comment.update import update_comment
from app.views.comment.delete import delete_comment

app_name = "comment"

urlpatterns = [

    # -------------------------------------------------------
    # Create
    # -------------------------------------------------------

    path(
        "post/<uuid:post_id>/create/",
        create_comment,
        name="create",
    ),

    # -------------------------------------------------------
    # Update
    # -------------------------------------------------------

    path(
        "<uuid:comment_id>/edit/",
        update_comment,
        name="update",
    ),

    # -------------------------------------------------------
    # Delete
    # -------------------------------------------------------

    path(
        "<uuid:comment_id>/delete/",
        delete_comment,
        name="delete",
    ),

]