from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

from app.core.models import (
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel,
)

from app.core.validators import validate_avatar, validate_cover


# -------------------------------------------------------
# Custom User Manager
# -------------------------------------------------------

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


# -------------------------------------------------------
# Custom User
# -------------------------------------------------------

class CustomUser(AbstractUser):
    """
    Core Identity Model
    """

    email = models.EmailField(
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    EMAIL_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
        ]

    def __str__(self):
        return self.username


# -------------------------------------------------------
# User Profile
# -------------------------------------------------------

class UserProfile(
    UUIDModel,
    TimeStampedModel,
):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        validators=[validate_avatar],
        blank=True,
        null=True,
    )

    cover_image = models.ImageField(
        upload_to="covers/%Y/%m/",
        validators=[validate_cover],
        blank=True,
        null=True,
    )

    bio = models.CharField(
        max_length=160,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    location = models.CharField(
        max_length=120,
        blank=True,
    )

    profession = models.CharField(
        max_length=120,
        blank=True,
    )

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return self.user.username


# -------------------------------------------------------
# Verification
# -------------------------------------------------------

class UserVerification(
    UUIDModel,
    TimeStampedModel,
):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="verification",
    )

    is_verified = models.BooleanField(
        default=False,
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    otp_secret = models.CharField(
        max_length=128,
        blank=True,
    )

    class Meta:
        db_table = "user_verifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Verification: {self.user.username}"


# -------------------------------------------------------
# Activity
# -------------------------------------------------------

class UserActivity(
    UUIDModel,
    TimeStampedModel,
):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="activity",
    )

    is_online = models.BooleanField(
        default=False,
    )

    last_seen = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    class Meta:
        db_table = "user_activity"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Activity: {self.user.username}"


# -------------------------------------------------------
# Security
# -------------------------------------------------------

class UserSecurity(
    UUIDModel,
    TimeStampedModel,
):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="security",
    )

    password_reset_requested_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    failed_login_attempts = models.PositiveIntegerField(
        default=0,
    )

    account_locked_until = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
    )

    class Meta:
        db_table = "user_security"
        ordering = ["-created_at"]

    @property
    def is_locked(self):
        if self.account_locked_until and timezone.now() < self.account_locked_until:
            return True
        return False

    def __str__(self):
        return f"Security: {self.user.username}"


# -------------------------------------------------------
# Follow Relationship
# -------------------------------------------------------

class UserFollow(
    UUIDModel,
    TimeStampedModel,
):

    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="following",
    )

    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        db_table = "user_follows"
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "follower",
                    "following",
                ],
                name="unique_follow_relation",
            ),
            models.CheckConstraint(
                condition=~models.Q(follower=models.F("following")),
                name="prevent_self_follow",
            ),
        ]

        indexes = [
            models.Index(
                fields=["follower"],
            ),
            models.Index(
                fields=["following"],
            ),
        ]

    def __str__(self):
        return f"{self.follower} -> {self.following}"