from django.db import models

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
)

from .user import CustomUser
from .post import Post


class Bookmark(
    UUIDModel,
    TimeStampedModel,
):
    """
    Saved Posts
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )

    class Meta:

        db_table = "bookmarks"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "post",
                ],
                name="unique_bookmark",
            )
        ]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["post"]),
        ]

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.id}"