import datetime

from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=15)
    publish_date = models.DateTimeField("date published")
    body_content = models.CharField(max_length=500)

    def __repr__(self):
        return f"Post(title={self.title!r}, body_content={self.body_content!r}, publish_date={self.publish_date!r}"

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.publish_date <= now
