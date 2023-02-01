from django.contrib import admin

from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    # type the title of a new post, the slug field is filled in automatically.
    prepopulated_fields = {"slug": ("title",)}
    # raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
