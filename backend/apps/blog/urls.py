from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    # post views
    path("", views.PostListView.as_view(), name="post_list"),
    path(
        "tag/<slug:tag_slug>/",
        views.PostListView.post_list_by_tag,
        name="post_list_by_tag",
    ),
    path(
        "search/",
        views.PostListView.post_search,
        name="post_search",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>",
        views.PostListDetailView.post_detail,
        name="post_detail",
    ),
    path(
        "<int:post_id>/share/",
        views.PostListDetailView.post_share,
        name="post_share",
    ),
    path(
        "<int:post_id>/comment/",
        views.PostListDetailView.as_view(),
        name="post_comment",
    ),
    # Navigate to http://127.0.0.1:8000/blog/feed/ in your browser. You should now see the RSS feed,
    # including the last five blog posts.
    path("feed/", LatestPostsFeed(), name="post_feed"),
]
