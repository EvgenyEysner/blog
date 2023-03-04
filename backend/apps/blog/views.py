from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from taggit.models import Tag

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    # Django’s ListView generic view passes the page requested in a variable called page_obj .
    paginate_by = 3
    template_name = "blog/post/list.html"

    # post_list_by_tag view let users list all posts tagged with a specific tag.
    @staticmethod
    def post_list_by_tag(request, tag_slug=None):
        post_list = Post.published.all()
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post_list = post_list.filter(tags__in=[tag])
        # Pagination with 3 posts per page
        paginator = Paginator(post_list, 3)
        page_number = request.GET.get("page", 1)
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            # If page_number is not an integer deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page_number is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
        return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


class PostListDetailView(DetailView, FormView):
    model = Post
    form_class = CommentForm
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        pk = self.kwargs.get("post_id")
        self.object.post_id = pk
        self.object.save()
        return super().form_valid(form)

    @staticmethod
    def post_detail(request, year, month, day, post):
        post = get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day,
        )
        # List of active comments for this post
        comments = post.comments.filter(active=True)
        # Form for users to comment
        form = CommentForm()
        return render(
            request,
            "blog/post/detail.html",
            {"post": post, "comments": comments, "form": form},
        )

    @staticmethod
    def post_share(request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        sent = False
        if request.method == "POST":
            # Form was submitted
            form = EmailPostForm(request.POST)
            if form.is_valid():
                # Form fields passed validation
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url())
                subject = f"{cd['name']} recommend you read {post.title}"
                message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']}"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
                sent = True
        else:
            form = EmailPostForm()
        return render(
            request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
        )


### ----------------- Other ways to implement ------------------------------------------------------------------- ###

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


# @require_POST
# def post_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
#     if request.method == "POST":
#         # Form was submitted
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             # Create a Comment object without saving it to the database
#             # If you call it using commit=False , the model instance is created but not saved to
#             # the database. This allows us to modify the object before finally saving it.
#             comment = form.save(commit=False)
#             # Assign the post to the comment
#             comment.post = post
#             # Save the comment to the database
#             comment.save()
#     else:
#         form = CommentForm()
#     return render(
#         request,
#         "blog/post/comment.html",
#         {"post": post, "form": form, "comment": comment},
#     )
