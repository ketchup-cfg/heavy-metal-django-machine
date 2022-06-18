import datetime

from django.utils import timezone

from posts.models import Post


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
