from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from blog.managers import PublishedManager

User = get_user_model()


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", _("DRAFT")
        PUBLISHED = "PB", _("PUBLISHED")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    # create SEO-friendly URLs for posts By using unique_for_date , the slug field
    # is now required to be unique for the date stored in the publish field.
    slug = models.SlugField(max_length=250, unique_for_date="publish")
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

    # The reverse() function will build the URL dynamically using the URL name defined in the URL
    # patterns.
    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )
