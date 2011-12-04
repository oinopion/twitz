import pytz
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

TIME_ZONE_CHOICES = zip(pytz.common_timezones, pytz.common_timezones)

def validate_time_zone(time_zone):
    if time_zone not in pytz.common_timezones:
        raise ValidationError('%s is not valid time zone' % time_zone)


class Profile(models.Model):
    utc = pytz.utc
    common_timezones = pytz.common_timezones

    user = models.OneToOneField(User)
    time_zone = models.CharField(max_length=200, choices=TIME_ZONE_CHOICES,
                                 validators=[validate_time_zone], blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
