from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from posts.models import Post


class PostIndexView(ListView):
    template_name = "posts/index.html"
    context_object_name = "latest_posts_list"

    def get_queryset(self) -> QuerySet[Post]:
        """
        Return the last five published post (not including those set to be
        published in the future).
        """
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by(
            "-publish_date"
        )[:5]


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/detail.html"

    def get_queryset(self) -> QuerySet[Post]:
        """
        Excludes any posts that aren't published yet.
        """
        return Post.objects.filter(publish_date__lte=timezone.now())


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "body_content", "publish_date"]
    template_name = "posts/detail.html"


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/detail.html"
    success_url = reverse_lazy("posts:index")
