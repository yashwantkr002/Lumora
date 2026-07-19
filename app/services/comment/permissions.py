"""
===========================================================
File: app/services/comment/permissions.py
===========================================================

PURPOSE

Centralized authorization for comments.

Used by:

• CommentCreateService
• CommentUpdateService
• CommentDeleteService
• CommentDetailService

===========================================================
"""

from django.core.exceptions import PermissionDenied

from app.models.comment import Comment
from app.models.user import CustomUser


class CommentPermissionService:
    """
    Handles authorization for comment operations.
    """

    # -------------------------------------------------------
    # Owner
    # -------------------------------------------------------

    @staticmethod
    def is_owner(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> bool:
        """
        Return True if the user owns the comment.
        """

        return comment.author_id == user.id

    # -------------------------------------------------------
    # View Permission
    # -------------------------------------------------------

    @staticmethod
    def can_view(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> bool:
        """
        Determine whether a user can view a comment.
        """

        # Owner can always view

        if CommentPermissionService.is_owner(
            comment=comment,
            user=user,
        ):
            return True

        # Hidden comments are only visible
        # to their author.

        if comment.is_hidden:

            return False

        # Otherwise visible.

        return True

    # -------------------------------------------------------
    # Edit Permission
    # -------------------------------------------------------

    @staticmethod
    def can_edit(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> bool:
        """
        Determine whether a user can edit a comment.
        """

        return CommentPermissionService.is_owner(
            comment=comment,
            user=user,
        )

    # -------------------------------------------------------
    # Delete Permission
    # -------------------------------------------------------

    @staticmethod
    def can_delete(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> bool:
        """
        Determine whether a user can delete a comment.
        """

        return CommentPermissionService.is_owner(
            comment=comment,
            user=user,
        )

    # -------------------------------------------------------
    # Reply Permission
    # -------------------------------------------------------

    @staticmethod
    def can_reply(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> bool:
        """
        Determine whether a user can reply
        to a comment.
        """

        if comment.is_hidden:

            return False

        return True

    # -------------------------------------------------------
    # Require View
    # -------------------------------------------------------

    @staticmethod
    def require_view_permission(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> None:
        """
        Raise PermissionDenied if the user
        cannot view the comment.
        """

        if not CommentPermissionService.can_view(
            comment=comment,
            user=user,
        ):

            raise PermissionDenied(
                "You do not have permission to view this comment."
            )

    # -------------------------------------------------------
    # Require Edit
    # -------------------------------------------------------

    @staticmethod
    def require_edit_permission(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> None:
        """
        Raise PermissionDenied if the user
        cannot edit the comment.
        """

        if not CommentPermissionService.can_edit(
            comment=comment,
            user=user,
        ):

            raise PermissionDenied(
                "You do not have permission to edit this comment."
            )

    # -------------------------------------------------------
    # Require Delete
    # -------------------------------------------------------

    @staticmethod
    def require_delete_permission(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> None:
        """
        Raise PermissionDenied if the user
        cannot delete the comment.
        """

        if not CommentPermissionService.can_delete(
            comment=comment,
            user=user,
        ):

            raise PermissionDenied(
                "You do not have permission to delete this comment."
            )

    # -------------------------------------------------------
    # Require Reply
    # -------------------------------------------------------

    @staticmethod
    def require_reply_permission(
        *,
        comment: Comment,
        user: CustomUser,
    ) -> None:
        """
        Raise PermissionDenied if the user
        cannot reply to the comment.
        """

        if not CommentPermissionService.can_reply(
            comment=comment,
            user=user,
        ):

            raise PermissionDenied(
                "You cannot reply to this comment."
            )