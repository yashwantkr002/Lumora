"""
===========================================================
File: app/services/comment/utils.py
===========================================================

PURPOSE

Shared utility methods for comments.

Used by:

• CommentCreateService
• CommentUpdateService
• CommentDeleteService

===========================================================
"""

from django.core.exceptions import ValidationError
from django.db.models import F

from app.models.comment import Comment
from app.models.post import Post


class CommentUtilsService:
    """
    Shared helper methods for comments.
    """

    # -------------------------------------------------------
    # Validate Parent
    # -------------------------------------------------------

    @staticmethod
    def validate_parent(
        *,
        post: Post,
        parent: Comment | None,
    ) -> None:
        """
        Ensure the parent comment belongs
        to the same post.
        """

        if parent is None:
            return

        if parent.post_id != post.id:

            raise ValidationError(
                "Parent comment must belong to the same post."
            )

    # -------------------------------------------------------
    # Increment Post Comments
    # -------------------------------------------------------

    @staticmethod
    def increment_post_comments(
        *,
        post: Post,
    ) -> None:
        """
        Increase the post comment counter.
        """

        Post.objects.filter(
            pk=post.pk,
        ).update(
            comments_count=F("comments_count") + 1,
        )

    # -------------------------------------------------------
    # Decrement Post Comments
    # -------------------------------------------------------

    @staticmethod
    def decrement_post_comments(
        *,
        post: Post,
    ) -> None:
        """
        Decrease the post comment counter.
        """

        Post.objects.filter(
            pk=post.pk,
        ).update(
            comments_count=F("comments_count") - 1,
        )

    # -------------------------------------------------------
    # Increment Reply Count
    # -------------------------------------------------------

    @staticmethod
    def increment_reply_count(
        *,
        parent: Comment | None,
    ) -> None:
        """
        Increase the parent's reply counter.
        """

        if parent is None:
            return

        Comment.objects.filter(
            pk=parent.pk,
        ).update(
            replies_count=F("replies_count") + 1,
        )

    # -------------------------------------------------------
    # Decrement Reply Count
    # -------------------------------------------------------

    @staticmethod
    def decrement_reply_count(
        *,
        parent: Comment | None,
    ) -> None:
        """
        Decrease the parent's reply counter.
        """

        if parent is None:
            return

        Comment.objects.filter(
            pk=parent.pk,
        ).update(
            replies_count=F("replies_count") - 1,
        )

    # -------------------------------------------------------
    # Mark Edited
    # -------------------------------------------------------

    @staticmethod
    def mark_as_edited(
        *,
        comment: Comment,
    ) -> None:
        """
        Mark a comment as edited.
        """

        comment.is_edited = True

    # -------------------------------------------------------
    # Normalize Content
    # -------------------------------------------------------

    @staticmethod
    def normalize_content(
        *,
        content: str,
    ) -> str:
        """
        Normalize comment content.
        """

        return " ".join(
            content.strip().split()
        )