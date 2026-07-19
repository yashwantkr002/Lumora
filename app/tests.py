from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from app.models.story import Story
from app.models.user import UserProfile


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
