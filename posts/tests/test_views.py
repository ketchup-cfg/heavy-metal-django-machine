from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from posts.models import Post
from posts.tests import create_post


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

    def test_post_does_not_exist(self):
        """
        Ensure that the detail view returns a 404 error when an ID for a nonexistant
        post is provided.
        """
        expected = 404
        post = create_post(title="New post.", body_content="News!", days=-30)
        post_id = post.id

        post.delete()
        url = reverse("posts:detail", args=(post_id,))
        response = self.client.get(url)
        actual = response.status_code

        self.assertEqual(expected, actual)


class PostCreateViewTests(TestCase):
    def test_create_valid_post(self):
        """
        Ensure that the create view successfully create a post when valid data is
        provided, and that it shows the new data on the detail view page.
        """
        post_title = "Post title"
        post_body = "Some content"

        url = reverse("posts:create")
        response = self.client.post(
            url,
            {
                "title": post_title,
                "body_content": post_body,
                "publish_date": timezone.now(),
            },
            follow=True,
        )

        self.assertContains(response, post_title)
        self.assertContains(response, post_body)


class PostUpdateViewTests(TestCase):
    def test_update_valid_post(self):
        """
        Ensure that the update view successfully updates the data for a post when valid
        data is provided, and that it shows the updated data on the detail view page.
        """
        post = create_post(title="New post.", body_content="News!", days=-30)
        post.title = "Valid post."
        post.body_content = "Some valid content."

        url = reverse("posts:update", args=(post.id,))
        response = self.client.post(
            url,
            {
                "title": post.title,
                "body_content": post.body_content,
                "publish_date": post.publish_date,
            },
            follow=True,
        )

        self.assertContains(response, post.title)
        self.assertContains(response, post.body_content)

    def test_update_nonexistant_post(self):
        """
        Ensure that the update view returns a 404 response status code when called for
        post that does not exist.
        """
        expected = 404
        post = create_post(title="New post.", body_content="News!", days=-30)
        post.title = "Valid post."
        post.body_content = "Some valid content."
        post_id = post.id

        post.delete()
        url = reverse("posts:update", args=(post_id,))
        response = self.client.post(
            url,
            {
                "title": post.title,
                "body_content": post.body_content,
                "publish_date": post.publish_date,
            },
            follow=True,
        )
        actual = response.status_code

        self.assertEqual(expected, actual)


class PostDeleteViewTests(TestCase):
    def test_delete_existing_post(self):
        """
        Ensure that the delete view successfully deletes the specified post when a
        valid post ID is provided.
        """
        post = create_post(title="New post.", body_content="News!", days=-30)

        delete_url = reverse("posts:delete", args=(post.id,))
        _ = self.client.delete(delete_url)

        with self.assertRaises(Post.DoesNotExist):
            _ = Post.objects.get(pk=post.id)

    def test_delete_nonexistant_post(self):
        """
        Ensure that the delete view returns a 404 when attempting to delete a post that
        does not exist.
        """
        expected = 404
        post = create_post(title="New post.", body_content="News!", days=-30)
        post_id = post.id

        post.delete()
        delete_url = reverse("posts:delete", args=(post_id,))
        response = self.client.delete(delete_url)
        actual = response.status_code

        self.assertEqual(expected, actual)
