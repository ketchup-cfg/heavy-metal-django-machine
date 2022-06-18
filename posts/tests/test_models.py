import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from posts.models import Post
from posts.tests import create_post


class PostModelTests(TestCase):
    def test_str_returns_post_title(self):
        """
        __str__ returns the title of the post.
        """
        post = create_post(title="New post.", body_content="Some content!", days=30)
        expected = post.title

        actual = str(post)

        self.assertEqual(expected, actual)

    def test_repr_returns_formatted_post(self):
        """
        __repr__ returns the expected representation of the post.
        """
        post = create_post(title="New post.", body_content="Some content!", days=30)
        expected = f"Post(title={post.title!r}, body_content={post.body_content!r}, publish_date={post.publish_date!r}"

        actual = repr(post)

        self.assertEqual(expected, actual)

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
        was_published_recently() returns True for posts whose publish_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_post = Post(publish_date=time)
        self.assertIs(recent_post.was_published_recently(), True)

    def test_get_absolute_url(self):
        """
        get_absolute_url() returns the expected URL for the post.
        """
        post = create_post(title="New post.", body_content="Some content!", days=30)
        expected = reverse("posts:detail", args=(post.id,))
        actual = post.get_absolute_url()
        self.assertEqual(expected, actual)
