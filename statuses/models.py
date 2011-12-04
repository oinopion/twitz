from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MaxLengthValidator



TIMELINE_LIMIT = 20

class StatusesManager(models.Manager):
    def timeline(self, max_items=TIMELINE_LIMIT):
        return self.order_by('-pub_date').select_related()[:max_items]

len_256 = MaxLengthValidator(256)

class Status(models.Model):
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=now, db_index=True)
    text = models.TextField(max_length=256, validators=[len_256])
    objects = StatusesManager()

    class Meta:
        verbose_name_plural = 'Statuses'
