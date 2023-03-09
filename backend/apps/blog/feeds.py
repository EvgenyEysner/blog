import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):
    """
    Django has a built-in syndication feed framework that you can use to dynamically generate RSS or Atom
    feeds in a similar manner to creating sitemaps using the site’s framework. A web feed is a data format
    (usually XML) that provides users with the most recently updated content. Users can subscribe to the
    feed using a feed aggregator, a software that is used to read feeds and get new content notifications.
    """

    title = "My blog"
    link = reverse_lazy("blog:post_list")
    description = "New posts of my blog."

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
