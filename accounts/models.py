import pytz
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

TIME_ZONE_CHOICES = zip(pytz.common_timezones, pytz.common_timezones)

class Profile(models.Model):
    utc = pytz.utc
    common_timezones = pytz.common_timezones

    user = models.OneToOneField(User)
    time_zone = models.CharField(max_length=200, choices=TIME_ZONE_CHOICES,
                                 blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
