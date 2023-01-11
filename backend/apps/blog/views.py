# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    # Django’s ListView generic view passes the page requested in a variable called page_obj .
    paginate_by = 3
    template_name = "blog/post/list.html"


class PostListDetailView(DetailView):
    pass


# def post_list(request):
#     post_list = Post.published.all()
#
#     # Pagination with 3 posts per page
#     # learn more about the Paginator class at https://docs.djangoproject.com/en/4.1/ref/
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get("page", 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # If page_number is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page_number is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, "blog/post/list.html", {"posts": posts})
#
#


# ToDo create class based View
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})
