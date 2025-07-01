from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser, list_display=[
    'username',
    'profile_picture',
    'bio',
    'website',
    'date_of_birth',
    'status',])
admin.site.register(Post, list_display=[
    'author',
    'caption',
    'image',
    'video',
    'media_type',
    'created_at',
])
admin.site.register(Comment, list_display=[
    'post',
    'author',
    'content',
    'created_at',
])
admin.site.register(Like, list_display=[
    'user',
    'post',
    'created_at',
])
admin.site.register(Follow, list_display=[
    'follower',
    'followed',
    'created_at',
])
admin.site.register(Notification, list_display=[
    'user',
    'type',
    'message',
    'created_at',
    'is_read',
])
admin.site.register(Message, list_display=[
    'conversation',
    'sender',
    'content',
    'created_at',
    'is_read',
])
admin.site.register(Story, list_display=[
    'user',
    'image',
    'video',
    'created_at',
    'expires_at',
])
admin.site.register(Conversation)