from django.contrib import admin

from app.models.user import UserActivity,UserVerification,UserProfile,UserFollow
from .models import *
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'caption',
        'visibility',
        'created_at',
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'post',
        'author',
        'content',
        'created_at',
    ]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'post',
        'created_at',
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'follower',
        'following',
        'created_at',
    ]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'recipient',
        'actor',
        'notification_type',
        'created_at',
        'is_read',
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'conversation',
        'sender',
        'content',
        'created_at',
        'seen',
    ]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'image',
        'video',
        'created_at',
        'expires_at',
    ]


admin.site.register(Conversation)

admin.site.register(UserActivity)
admin.site.register(UserVerification)
admin.site.register(UserProfile)
# admin.site.register(UserFollow)