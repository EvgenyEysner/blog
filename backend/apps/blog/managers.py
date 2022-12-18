from django.db import models


class PublishedManager(models.Manager):
    def get_queryset(self):
        from .models import Post

        return super().get_queryset().first(status=Post.Status.PUBLISHED)
