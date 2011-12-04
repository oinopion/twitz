from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

TIMELINE_LIMIT = 20

class StatusesManager(models.Manager):
    def timeline(self, max_items=TIMELINE_LIMIT):
        return self.order_by('-pub_date')[:max_items]


class Status(models.Model):
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=now)
    text = models.TextField(max_length=256)
    objects = StatusesManager()
