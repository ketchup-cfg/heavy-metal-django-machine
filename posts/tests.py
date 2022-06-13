import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


def create_post(title: str, body_content, days: int) -> Post:
    """
    Create a post with the given `title` and `body_content` and published the
    given number of `days` offset to now (negative for posts published
    in the past, positive for posts that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(
        title=title, body_content=body_content, publish_date=time
    )


class PostModelTests(TestCase):
    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() returns False for posts whose publish_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(publish_date=time)
        self.assertIs(future_post.was_published_recently(), False)

    def test_was_published_recently_with_old_post(self):
        """
        was_published_recently() returns False for posts whose publish_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_post = Post(publish_date=time)
        self.assertIs(old_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_post(self):
        """
        was_published_recently() returns True for post whose publish_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_post = Post(publish_date=time)
        self.assertIs(recent_post.was_published_recently(), True)


class PostIndexViewTests(TestCase):
    def test_past_post(self):
        """
        Posts with a publish_date in the past are displayed on the
        index page.
        """
        post = create_post(title="Past post.", body_content="old news!", days=-30)
        response = self.client.get(reverse("posts:index"))
        self.assertQuerysetEqual(
            response.context["latest_posts_list"],
            [post],
        )

    def test_future_post(self):
        """
        Posts with a publish_date in the future aren't displayed on
        the index page.
        """
        post = create_post(
            title="Future post.", body_content="This is breaking news!", days=30
        )
        response = self.client.get(reverse("posts:index"))
        self.assertNotContains(response, post.title)
        self.assertQuerysetEqual(response.context["latest_posts_list"], [])

    def test_future_post_and_past_post(self):
        """
        Even if both past and future posts exist, only past posts
        are displayed.
        """
        post = create_post(title="Past post.", body_content="old news!", days=-30)
        _ = create_post(
            title="Future post.", body_content="This is breaking news!", days=30
        )
        response = self.client.get(reverse("posts:index"))
        self.assertQuerysetEqual(
            response.context["latest_posts_list"],
            [post],
        )

    def test_two_past_posts(self):
        """
        The posts index page may display multiple posts.
        """
        first_post = create_post(
            title="Past post 1.", body_content="older news!", days=-30
        )
        second_post = create_post(
            title="Past post 2.", body_content="old news!", days=-5
        )
        response = self.client.get(reverse("posts:index"))
        self.assertQuerysetEqual(
            response.context["latest_posts_list"],
            [second_post, first_post],
        )


class PostDetailViewTests(TestCase):
    def test_future_post(self):
        """
        The detail view of a post with a publish_date in the future
        returns a 404 not found.
        """
        future_post = create_post(
            title="Future post.", body_content="This is breaking news!", days=5
        )
        url = reverse("posts:detail", args=(future_post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_post(self):
        """
        The detail view of a post with a publish_date in the past
        displays the post's text.
        """
        past_post = create_post(title="Past post.", body_content="older news!", days=-5)
        url = reverse("posts:detail", args=(past_post.id,))
        response = self.client.get(url)
        self.assertContains(response, past_post.title)


