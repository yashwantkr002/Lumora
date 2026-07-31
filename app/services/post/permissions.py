"""
===========================================================
File: app/services/post/permissions.py
===========================================================

PURPOSE

Centralized authorization for posts.

Used by:

• CreatePostService
• UpdatePostService
• DeletePostService
• DetailPostService
• FeedService
• Future APIs

===========================================================
"""

from django.core.exceptions import PermissionDenied

from app.models.post import Post
from app.models.user import CustomUser


class PostPermissionService:
    """
    Handles authorization for post operations.
    """

    # -------------------------------------------------------
    # Owner
    # -------------------------------------------------------

    @staticmethod
    def is_owner(
        *,
        post: Post,
        user: CustomUser,
    ) -> bool:
        """
        Return True if the user owns the post.
        """

        return post.author_id == user.id

    # -------------------------------------------------------
    # View Permission
    # -------------------------------------------------------

    @staticmethod
    def can_view(
        *,
        post: Post,
        user: CustomUser,
    ) -> bool:
        """
        Determine whether a user can view a post.
        """

        # Owner always has access

        if PostPermissionService.is_owner(
            post=post,
            user=user,
        ):
            return True

        # Public

        if post.visibility == Post.Visibility.PUBLIC:
            return True

        # Followers

        if (
            post.visibility
            == Post.Visibility.FOLLOWERS
        ):

            return post.author.followers.filter(
                follower=user,
            ).exists()

        # Private

        return False

    # -------------------------------------------------------
    # Edit Permission
    # -------------------------------------------------------

    @staticmethod
    def can_edit(
        *,
        post: Post,
        user: CustomUser,
    ) -> bool:
        """
        Determine whether a user can edit a post.
        """

        return PostPermissionService.is_owner(
            post=post,
            user=user,
        )

    # -------------------------------------------------------
    # Delete Permission
    # -------------------------------------------------------

    @staticmethod
    def can_delete(
        *,
        post: Post,
        user: CustomUser,
    ) -> bool:
        """
        Determine whether a user can delete a post.
        """

        return PostPermissionService.is_owner(
            post=post,
            user=user,
        )

    # -------------------------------------------------------
    # Require View
    # -------------------------------------------------------

    @staticmethod
    def require_view_permission(
        *,
        post: Post,
        user: CustomUser,
    ) -> None:
        """
        Raise PermissionDenied if user
        cannot view the post.
        """

        if not PostPermissionService.can_view(
            post=post,
            user=user,
        ):

            raise PermissionDenied(
                "You do not have permission to view this post."
            )

    # -------------------------------------------------------
    # Require Edit
    # -------------------------------------------------------

    @staticmethod
    def require_edit_permission(
        *,
        post: Post,
        user: CustomUser,
    ) -> None:
        """
        Raise PermissionDenied if user
        cannot edit the post.
        """

        if not PostPermissionService.can_edit(
            post=post,
            user=user,
        ):

            raise PermissionDenied(
                "You do not have permission to edit this post."
            )

    # -------------------------------------------------------
    # Require Delete
    # -------------------------------------------------------

    @staticmethod
    def require_delete_permission(
        *,
        post: Post,
        user: CustomUser,
    ) -> None:
        """
        Raise PermissionDenied if user
        cannot delete the post.
        """

        if not PostPermissionService.can_delete(
            post=post,
            user=user,
        ):

            raise PermissionDenied(
                "You do not have permission to delete this post."
            )