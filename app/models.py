from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# Validation for file size
def validate_file_size(file):
    # 10 MB 20mb according to required
    max_size_kb = 10240  # 10 MB
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"File size cannot exceed {max_size_kb} KB.")
# Custom User Model
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, validators=[validate_file_size])
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    date_of_birth = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')], default='offline')
    otp_secret = models.CharField(max_length=100, null=True, blank=True)
    password_reset_requested_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.username

# Tag Model for Hashtags
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Post Model
class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    video = models.FileField(upload_to='reels/', null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def like_count(self):
        """Returns the total number of likes for the post."""
        return self.like_set.count()

    def is_liked_by(self, user):
        """Checks if a specific user has liked the post."""
        return self.like_set.filter(user=user).exists()

    def clean(self):
        """Validation for media type."""
        super().clean()
        max_size_kb = 10240  

        if self.media_type == 'image' and not self.image:
            raise ValidationError("Image is required for media_type 'image'.")
        if self.media_type == 'video' and not self.video:
            raise ValidationError("Video is required for media_type 'video'.")
        if self.image and self.video:
            raise ValidationError("A post can only have either an image or a video, not both.")
        if self.image and self.image.size > max_size_kb * 1024:
            raise ValidationError(f"Image size cannot exceed {max_size_kb} KB.")
        if self.video and self.video.size > max_size_kb * 1024:
            raise ValidationError(f"Video size cannot exceed {max_size_kb} KB.")

    def __str__(self):
        return f"{self.media_type.capitalize()} by {self.author.username}"

    class Meta:
        ordering = ['-created_at']

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']

# Like Model
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.caption}"

    class Meta:
        ordering = ['-created_at']
# Story Model
class Story(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/images/', null=True, blank=True)
    video = models.FileField(upload_to='stories/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    views = models.ManyToManyField(CustomUser, related_name='viewed_stories', blank=True)

    def clean(self):
        if not self.image and not self.video:
            raise ValidationError("A story must have either an image or a video.")

    def __str__(self):
        return f"Story by {self.user.username}"

    class Meta:
        ordering = ['-created_at']

# Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']

# Follow Model
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    class Meta:
        ordering = ['-created_at']

# Conversation Model
class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {', '.join([user.username for user in self.participants.all()])}"

# Message Model
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username}"

    class Meta:
        ordering = ['-created_at']
