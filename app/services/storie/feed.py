import logging
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone
from app.models import user
from app.models.story import Story
from django.contrib.auth.models import User
User = get_user_model()
logger = logging.getLogger(__name__)


class FeedStoryService:
    """
    Handles fetching and filtering active stories for a user's feed.
    """

    @staticmethod
    def get_feed_stories(user=user) -> QuerySet[Story]:
        """
        Fetch active stories from users that the given user follows,
        including their own active stories. Order by most recent.
        """
        now = timezone.now()

        # 1. उन सभी यूज़र्स की IDs निकालो जिन्हें करंट यूज़र फ़ॉलो करता है
        # तुम्हारे CustomUser मॉडल में 'following' ManyToMany relation है
        followed_users_ids = user.following.values_list("pk", flat=True)

        # 2. फ़ॉलो किए गए यूज़र्स और खुद की आईडी को एक लिस्ट में कंबाइन करो
        # सोशल मीडिया पर यूज़र को खुद की स्टोरीज़ भी फ़ीड में दिखती हैं
        feed_user_ids = list(followed_users_ids) + [user.pk]

        # 3. डेटाबेस से सिर्फ एक्टिव स्टोरीज़ फ़ेच करो
        # select_related('user') इस्तेमाल किया है ताकि टेम्पलेट में user.username रेंडर करते वक्त N+1 क्वेरी न बने
        stories = (
            Story.objects.filter(
                user_id__in=feed_user_ids,
                expires_at__gt=now
            )
            .select_related("user")
            .order_by("-created_at")
        )

        # 4. स्ट्रक्चर्ड लॉगिंग (बिना PII लीक किए)
        logger.info(
            "Feed stories fetched successfully.",
            extra={
                "user_id": user.id,
                "stories_count": stories.count(),
            },
        )

        return stories