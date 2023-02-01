from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from blog.managers import PublishedManager

User = get_user_model()


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", _("DRAFT")
        PUBLISHED = "PB", _("PUBLISHED")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    # create SEO-friendly URLs for posts By using unique_for_date , the slug field
    # is now required to be unique for the date stored in the published field.
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    publish = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Veröffentlicht am")
    )
    created = models.DateTimeField(default=timezone.now, verbose_name=_("Erstellt am"))
    updated = models.DateTimeField(auto_now_add=True, verbose_name=_("Aktualisiert am"))
    title = models.CharField(verbose_name=_("Überschrift"), max_length=250)
    body = models.TextField(verbose_name=_("Text"))
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("Status"),
    )
    rating = models.IntegerField(default=0, verbose_name="Raiting")
    likes = models.IntegerField(default=0, verbose_name="Gefällt mir")
    dislikes = models.IntegerField(default=0, verbose_name="Gefällt mir nicht")

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


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80, verbose_name="Name")
    email = models.EmailField()
    body = models.TextField("Kommentar")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Kommentiert bei {self.name} zum {self.post}"
