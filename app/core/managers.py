from django.db import models


class ActiveManager(models.Manager):
    """
    Returns only active (non-soft-deleted) objects.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)