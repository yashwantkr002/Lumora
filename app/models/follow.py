from .user import UserFollow

Follow = UserFollow

__all__ = [
    "UserFollow",
    "Follow",
]

# follower = models.ForeignKey(
#     CustomUser,
#     related_name="following",
# )

# following = models.ForeignKey(
#     CustomUser,
#     related_name="followers",
# )