import hashlib
from datetime import timedelta
from unittest.mock import Mock, patch

import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from app.core.storage.cloudinary import CloudinaryStorage
from app.core.storage.local import LocalStorage
from app.models.conversation import Conversation
from app.models.notification import Notification
from app.models.post import Post
from app.models.story import Story
from app.models.user import UserProfile
from app.services.chat.message import MessageService
from app.services.like.toggle import LikeToggleService
from app.services.media.upload_service import UploadService
from app.services.post.create import CreatePostService


class MediaServiceTests(TestCase):
    @override_settings(MEDIA_UPLOAD_PATHS={"avatars": "uploads/profile/avatars", "posts": "uploads/posts"})
    def test_local_storage_upload_uses_configured_folder_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.settings(
                MEDIA_ROOT=temp_dir,
                STORAGES={
                    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
                },
            ):
                storage = LocalStorage()
                uploaded_file = SimpleUploadedFile(
                    "avatar.png",
                    b"avatar-bytes",
                    content_type="image/png",
                )

                result = storage.upload(file=uploaded_file, folder="avatars")

                self.assertTrue(result.path.startswith("uploads/profile/avatars/"))
                self.assertTrue(result.path.endswith(".png"))

    @patch("app.core.storage.cloudinary.CloudinaryStorage.upload", return_value=Mock(path="avatars/test-avatar.png", provider="cloudinary"))
    def test_upload_media_to_field_uses_storage_and_sets_name(self, upload_mock):
        uploaded_file = SimpleUploadedFile(
            "avatar.png",
            b"file-bytes",
            content_type="image/png",
        )

        service = UploadService()
        result = service.upload(file=uploaded_file, folder="avatars")

        self.assertEqual(result.path, "avatars/test-avatar.png")
        self.assertEqual(result.provider, "cloudinary")
        upload_mock.assert_called_once()

    @patch("app.core.storage.cloudinary.cloudinary.uploader.upload", return_value={"public_id": "avatars/avatar", "secure_url": "https://example.com/avatar.png", "resource_type": "image", "bytes": 123, "width": 100, "height": 100, "version": 1, "format": "png"})
    def test_cloudinary_upload_uses_deterministic_public_id(self, upload_mock):
        storage = CloudinaryStorage()
        uploaded_file = SimpleUploadedFile(
            "avatar.png",
            b"same-bytes",
            content_type="image/png",
        )

        storage.upload(file=uploaded_file, folder="avatars")

        expected_digest = hashlib.sha256(b"same-bytes").hexdigest()[:16]
        self.assertEqual(
            upload_mock.call_args.kwargs["public_id"],
            f"uploads/profile/avatars/avatar-{expected_digest}",
        )

    @patch("app.core.storage.cloudinary.cloudinary.uploader.upload", return_value={"public_id": "posts/post", "secure_url": "https://example.com/post.png", "resource_type": "image", "bytes": 123, "width": 100, "height": 100, "version": 1, "format": "png"})
    def test_cloudinary_upload_uses_image_resource_type_for_images(self, upload_mock):
        storage = CloudinaryStorage()
        uploaded_file = SimpleUploadedFile(
            "photo.png",
            b"image-bytes",
            content_type="image/png",
        )

        storage.upload(file=uploaded_file, folder="posts")

        self.assertEqual(upload_mock.call_args.kwargs["resource_type"], "image")
        uploaded_payload = upload_mock.call_args.args[0]
        uploaded_payload.seek(0)
        self.assertEqual(uploaded_payload.read(), b"image-bytes")

    @patch("app.core.storage.cloudinary.CloudinaryStorage.upload", return_value=Mock(path="posts/test.png", provider="cloudinary"))
    def test_create_post_media_uploads_once_per_file(self, upload_mock):
        author = get_user_model().objects.create_user(
            email="postmedia@example.com",
            username="postmedia",
            password="strongpass123",
        )
        post = Post.objects.create(author=author, caption="Media test")
        uploaded_file = SimpleUploadedFile(
            "photo.png",
            b"file-bytes",
            content_type="image/png",
        )

        CreatePostService._save_media(
            post=post,
            media_files=[uploaded_file],
        )

        self.assertEqual(post.media.count(), 1)
        upload_mock.assert_called_once()


class StoryDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="story@example.com",
            username="storyuser",
            password="strongpass123",
        )
        UserProfile.objects.create(user=self.user)
        self.story = Story.objects.create(
            author=self.user,
            media_type=Story.IMAGE,
            caption="A test story",
            expires_at=timezone.now() + timedelta(hours=1),
        )

    def test_story_detail_renders_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("story_detail", kwargs={"story_id": self.story.id}),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A test story")


class AuthImportTests(TestCase):
    def test_auth_package_exports_social_login_views(self):
        from app.views import auth as auth_views

        self.assertTrue(hasattr(auth_views, "social_login"))
        self.assertTrue(hasattr(auth_views, "social_login_callback"))


class RegistrationViewTests(TestCase):
    def test_registration_logs_new_user_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(email="new@example.com")
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))


class ChatMessageServiceTests(TestCase):
    def test_send_message_returns_serialized_payload(self):
        user = get_user_model().objects.create_user(
            email="chat@example.com",
            username="chatuser",
            password="strongpass123",
        )
        conversation = Conversation.objects.create(created_by=user)
        conversation.participants.add(user)

        payload = MessageService.send_message(
            conversation=conversation,
            sender=user,
            content="hello world",
        )

        self.assertEqual(payload["content"], "hello world")
        self.assertEqual(payload["sender_name"], user.username)
        self.assertEqual(payload["conversation_id"], str(conversation.id))


class NotificationServiceTests(TestCase):
    def test_liking_a_post_creates_a_notification_for_the_author(self):
        actor = get_user_model().objects.create_user(
            email="actor@example.com",
            username="actor",
            password="strongpass123",
        )
        author = get_user_model().objects.create_user(
            email="author@example.com",
            username="author",
            password="strongpass123",
        )
        post = Post.objects.create(author=author, caption="A test post")

        result = LikeToggleService.toggle_like(post=post, user=actor)

        self.assertTrue(result["liked"])
        notification = Notification.objects.get(recipient=author, actor=actor)
        self.assertEqual(notification.notification_type, Notification.LIKE)
        self.assertFalse(notification.is_read)


class LikeViewTests(TestCase):
    def test_like_toggle_view_returns_json_and_updates_count(self):
        user = get_user_model().objects.create_user(
            email="liker@example.com",
            username="liker",
            password="strongpass123",
        )
        author = get_user_model().objects.create_user(
            email="author2@example.com",
            username="author2",
            password="strongpass123",
        )
        post = Post.objects.create(author=author, caption="Like me")

        self.client.force_login(user)
        response = self.client.post(
            reverse("like:toggle", kwargs={"post_id": post.id}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertTrue(response.json()["liked"])
        self.assertEqual(response.json()["likes_count"], 1)


class PostDetailViewTests(TestCase):
    def test_post_detail_page_renders_for_authenticated_user(self):
        user = get_user_model().objects.create_user(
            email="detailviewer@example.com",
            username="detailviewer",
            password="strongpass123",
        )
        author = get_user_model().objects.create_user(
            email="detailauthor@example.com",
            username="detailauthor",
            password="strongpass123",
        )
        post = Post.objects.create(author=author, caption="Visible post")

        self.client.force_login(user)
        response = self.client.get(
            reverse("post:detail", kwargs={"post_id": post.id}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visible post")
