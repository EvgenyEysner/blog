from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from blog.managers import PublishedManager

User = get_user_model()


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", _("DRAFT")
        PUBLISH = "PB", _("PUBLISHED")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    slug = models.SlugField(max_length=250)
    publish = models.DateTimeField(auto_now_add=True, verbose_name=_(""))
    created = models.DateTimeField(default=timezone.now, verbose_name="")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="")
    title = models.CharField("Заголовок", max_length=250)
    body = models.TextField("Текст")
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    # rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    # likes = models.IntegerField(default=0, verbose_name="Понравилось")
    # dislikes = models.IntegerField(default=0, verbose_name="Не понравилось")

    published = PublishedManager()

    class Meta:
        ordering = ["-publish"]

        # This will improve performance for queries filtering or ordering results by this field
        # https://docs.djangoproject.com/en/4.1/ref/models/indexes/
        # Index ordering is not supported on MySQL. If using MySQL for the database,
        # a descending index will be created as a normal index.
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title
